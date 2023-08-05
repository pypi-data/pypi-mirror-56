"""Model training/evaluation base interface module.

This module contains the interface required to train and/or evaluate a model based on different tasks. The trainers
based on this interface are instantiated in launched sessions based on configuration dictionaries.
"""
import functools
import json
import logging
import math
import os
import platform
import random
import time
from abc import abstractmethod
from copy import deepcopy
from typing import Any, AnyStr, Optional  # noqa: F401

import cv2 as cv
import numpy as np
import torch
import torch.optim

import thelper.typedefs as typ  # noqa: F401
import thelper.utils

logger = logging.getLogger(__name__)


class Trainer:
    """Abstract trainer interface that defines basic session i/o and setup operations.

    This interface defines the general behavior of a training session which includes configuration parsing, tensorboard
    setup, metrics and goal setup, and loss/optimizer setup. It also provides utilities for uploading models and tensors
    on specific devices, and for saving the state of a session. This interface should be specialized for every task by
    implementing the ``train_epoch`` and ``eval_epoch`` functions in a derived class. For better support from visualization
    utilities, the derived class should also implement ``to_tensor``. See :class:`thelper.train.classif.ImageClassifTrainer`
    for a complete example.

    Any trainer derived from this class will alternate between training and validation epochs. It will also support
    post-training (final) evaluation using a separate test set. If requested, visualizations can be computed after
    the validation epoch during training (e.g. sample activation maps, or t-SNE plots). See :mod:`thelper.viz` for
    more information on these.

    The main parameters that will be parsed by this interface from a configuration dictionary are the following:

    - ``epochs`` (mandatory if training): number of epochs to train for; one epoch is one iteration over all mini-batches.
    - ``optimization`` (mandatory if training): sub-dictionary containing types and extra parameters required for
      instantiating the loss, optimizer, and scheduler objects. See the code of each related loading function for more
      information on special parameters.
    - ``save_freq`` (optional, default=1): checkpoint save frequency (will save every epoch multiple of given number).
    - ``save_raw`` (optional, default=True): specifies whether to save raw types or thelper objects in checkpoints.
    - ``use_tbx`` (optional, default=False): defines whether to use tensorboardX writers for logging or not.
    - ``device`` (optional): specifies which device to train/evaluate the model on (default=all available).
    - ``metrics``: list of metrics to instantiate and update during training/evaluation; see related loading function for
      more information.
    - ``monitor``: specifies the name of the metric that should be monitored on the validation set for model improvement.

    Example configuration file::

        # ...
        "trainer": {
            # type of trainer to instantiate (linked to task type)
            "type": "thelper.train.ImageClassifTrainer",
            # train for 40 epochs
            "epochs": 40,
            # save every 5 epochs
            "save_freq": 5,
            # monitor validation accuracy and save best model based on that
            "monitor": "accuracy",
            # optimization parameters block
            "optimization": {
                # all types & params below provided by PyTorch
                "loss": {
                    "type": "torch.nn.CrossEntropyLoss"
                },
                "optimizer": {
                    "type": "torch.optim.SGD",
                    "params": {
                        "lr": 0.1,
                        "momentum": 0.9,
                        "weight_decay": 1e-06,
                        "nesterov": true
                    }
                },
                "scheduler": {
                    "type": "torch.optim.lr_scheduler.StepLR",
                    "params": {
                        "step_size": 10,
                        "step_size": 0.1
                    }
                }
            },
            # visualization block (optional)
            "viz": {
                # multiple visualization techniques can be toggled by name
                "tsne": {
                    # visualization parameters would be provided here
                }
            },
            # in this example, we use two consumers in total
            # (one metric for monitoring, and one for logging)
            "metrics": {
                "accuracy": {
                    "type": "thelper.optim.Accuracy"
                },
                "fullreport": {
                    "type": "thelper.train.ClassifReport"
                }
            }
        }
        # ...

    Attributes:
        checkpoint_dir: session checkpoint output directory (located within the 'session directory').
        config: session configuration dictionary holding all original settings, including trainer configuration.
        devices: list of (cuda) device IDs to upload the model/tensors to; can be empty if only the CPU is available.
        epochs: number of epochs to train the model for.
        logger: used to output debug/warning/error messages to session log.
        model: reference to the model being trained or used for evaluation/prediction.
        monitor: name of the training/validation metric that should be monitored for model improvement.
        name: name of the session, used for printing and creating log folders.
        optimization_config: dictionary of optim-related parameters, parsed at training time.
        output_paths: map of session output paths where training/evaluation results should be saved.
        save_freq: frequency of checkpoint saves while training (i.e. save every X epochs).
        save_raw: specifies whether to save raw types or thelper objects in checkpoints.
        skip_eval_iter: number of evaluation iterations to skip (useful for resuming a session).
        skip_tbx_histograms: flag used to skip the generation of graph histograms in tbx (useful for large models).
        task: reference to the object used to specialize the model and that holds task metainformation.
        tbx_histogram_freq: frequency of tbx histogram saves while training (i.e. save every X epochs).
        use_tbx: defines whether to use tensorboardX writers for logging or not.
        writers: map of tbx writers used to save training/evaluation events.


    TODO: move static utils to their related modules

    .. seealso::
        | :class:`thelper.train.classif.ImageClassifTrainer`
        | :class:`thelper.train.segm.ImageSegmTrainer`
        | :class:`thelper.train.detect.ObjDetectTrainer`
        | :class:`thelper.train.regr.RegressionTrainer`
        | :func:`thelper.train.utils.create_trainer`
    """

    def __init__(self,
                 session_name,    # type: AnyStr
                 session_dir,     # type: AnyStr
                 model,           # type: thelper.typedefs.ModelType
                 task,            # type: thelper.tasks.Task
                 loaders,         # type: thelper.typedefs.MultiLoaderType
                 config,          # type: thelper.typedefs.ConfigDict
                 ckptdata=None    # type: Optional[thelper.typedefs.CheckpointContentType]
                 ):
        """Receives the trainer configuration dictionary, parses it, and sets up the session."""
        assert isinstance(model, (thelper.nn.Module, torch.nn.Module)), "unknown model object type"
        assert isinstance(task, thelper.tasks.Task), "unknown task object type"
        assert isinstance(loaders, (list, tuple, np.ndarray)) and len(loaders) == 3, "invalid loaders array"
        assert isinstance(config, dict), "invalid config type"
        self.task = task
        self.model = model
        self.config = config

        # parse basic training config args
        trainer_config = thelper.utils.get_key("trainer", config, msg="session config dictionary missing 'trainer' field")
        os.makedirs(session_dir, exist_ok=True)
        logs_dir = os.path.join(session_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        thelper.utils.init_logger()  # make sure all logging is initialized before attaching this part
        thelper.utils.save_env_list(os.path.join(logs_dir, "packages.log"))
        train_logger_path = os.path.join(logs_dir, "trainer.log")
        train_logger_format = logging.Formatter("[%(asctime)s - %(process)s] %(levelname)s : %(message)s")
        train_logger_fh = logging.FileHandler(train_logger_path)
        train_logger_fh.setLevel(logging.NOTSET)
        train_logger_fh.setFormatter(train_logger_format)
        self.logger = thelper.utils.get_class_logger()
        self.logger.addHandler(train_logger_fh)
        self.logger.info(f"created training log for session '{session_name}'")
        self.logger.debug(f"session directory = {os.path.abspath(session_dir)}")
        self.logger.debug(f"logs directory = {os.path.abspath(logs_dir)}")
        logstamp = thelper.utils.get_log_stamp()
        repover = thelper.__version__ + ":" + thelper.utils.get_git_stamp()
        self.logger.debug(f"logstamp = {logstamp}")
        self.logger.debug(f"version = {repover}")
        self.name = session_name
        self.epochs = 1
        self.save_freq = int(thelper.utils.get_key_def("save_freq", trainer_config, 1))
        assert self.save_freq >= 1, "checkpoint save frequency should be strictly positive integer"
        self.save_raw = thelper.utils.str2bool(thelper.utils.get_key_def("save_raw", trainer_config, True))
        self.checkpoint_dir = os.path.join(session_dir, "checkpoints")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        output_root_dir = thelper.utils.get_key_def("output_dir", trainer_config)
        if not output_root_dir:
            # append session name for cleaner TBX folder merging
            output_root_dir = os.path.join(session_dir, "output", self.name)
        assert isinstance(output_root_dir, str) and len(output_root_dir), "invalid output directory path"
        self.logger.debug(f"output directory = {os.path.abspath(output_root_dir)}")
        os.makedirs(output_root_dir, exist_ok=True)
        unique_output_dir = thelper.utils.get_key_def("unique_output_dir", trainer_config, True)
        assert isinstance(unique_output_dir, bool), "invalid unique_output_dir flag (should be bool)"
        self.logger.debug(f"output subdirectories {'will' if unique_output_dir else 'will not'} have unique names")
        devices_str = thelper.utils.get_key_def(["device", "devices", "train_device"], trainer_config, None)
        self.devices = self._load_devices(devices_str)
        self.skip_eval_iter = thelper.utils.get_key_def("skip_eval_iter", trainer_config, 0)

        # parse and prepare tbx stuff
        self.use_tbx = thelper.utils.str2bool(thelper.utils.get_key_def(["use_tbx", "tbx", "use_tb", "tb", "tensorboard"],
                                                                        trainer_config, False))
        if self.use_tbx:
            import tensorboardX  # todo: replace w/ pytorch's internal tbx @@@@@
            self.tbx = tensorboardX
            self.logger.debug(f"tensorboard init : tensorboard --logdir {os.path.abspath(output_root_dir)} --port <your_port>")
        self.skip_tbx_histograms = thelper.utils.str2bool(
            thelper.utils.get_key_def("skip_tbx_histograms", trainer_config, False))
        self.tbx_histogram_freq = int(thelper.utils.get_key_def("tbx_histogram_freq", trainer_config, 5))
        assert self.tbx_histogram_freq >= 1, "histogram output frequency should be strictly positive integer"
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.writers, self.output_paths = {}, {}
        for cname, loader in zip(["train", "valid", "test"], loaders):
            if loader:
                folder_name = f"{cname}-{str(platform.node())}-{timestr}" if unique_output_dir else cname
                self.output_paths[cname] = os.path.join(output_root_dir, folder_name)
                self.logger.debug(f"output {cname} directory = {os.path.abspath(self.output_paths[cname])}")
            else:
                self.output_paths[cname] = None
            self.writers[cname] = None  # will be instantiated only when needed based on above path

        # split loaders
        train_loader, valid_loader, test_loader = loaders
        assert (train_loader or valid_loader or test_loader), "must provide at least one loader with available data"
        self.train_loader, self.valid_loader, self.test_loader = train_loader, valid_loader, test_loader
        if train_loader:
            assert "epochs" in trainer_config and int(trainer_config["epochs"]) > 0, "bad trainer config epoch count"
            self.epochs = int(trainer_config["epochs"])
            # loading optimization stuff later since model needs to be on correct device
            self.optimization_config = thelper.utils.get_key_def("optimization", trainer_config, {})
        else:
            self.logger.info("no training data provided, will run a single epoch on valid/test data")

        # parse metrics
        assert "metrics" not in trainer_config or "base_metrics" not in trainer_config, \
            "trainer config should have only one of 'metrics' and 'base_metrics'"
        metrics = {}
        if "metrics" in trainer_config:
            self.logger.debug("loading metrics defined in trainer config")
            metrics = thelper.train.create_consumers(trainer_config["metrics"])
        elif "base_metrics" in trainer_config:
            self.logger.debug("loading base metrics defined in trainer config")
            metrics = thelper.train.create_consumers(trainer_config["base_metrics"])
        self.train_metrics, self.valid_metrics, self.test_metrics = \
            deepcopy(metrics), deepcopy(metrics), deepcopy(metrics)
        for skey, sval in zip(["train_metrics", "valid_metrics", "test_metrics"],
                              [self.train_metrics, self.valid_metrics, self.test_metrics]):
            if skey in trainer_config:
                new_metrics = thelper.train.create_consumers(trainer_config[skey])
                for mkey, mval in new_metrics.items():
                    assert mkey not in sval, f"metric name '{mkey}' duplicated in set '{skey}'"
                    sval[mkey] = mval
                for mkey, mval in sval.items():
                    self.logger.info(f"parsed metric '{mkey}': {str(mval)}")

        # check for monitored metric
        self.monitor, self.monitor_best, self.monitor_best_epoch = None, None, -1
        if "monitor" in trainer_config and trainer_config["monitor"]:
            self.monitor = trainer_config["monitor"]
            assert any([self.monitor in mset for mset in [self.train_metrics, self.valid_metrics]]), \
                f"metric with name '{self.monitor}' could not be found in training/validation metrics"
            metric = self.valid_metrics[self.monitor] if self.monitor in self.valid_metrics \
                else self.train_metrics[self.monitor]  # makes no sense to search for it in test metrics...
            assert isinstance(metric, thelper.optim.metrics.Metric), \
                "monitoring target should be an actual 'metric' class that returns a scalar!"
            assert metric.goal in [thelper.optim.Metric.minimize, thelper.optim.Metric.maximize], \
                "monitored metric does not return proper optimization goal"
            self.monitor_goal = metric.goal
            self.monitor_best = thelper.optim.Metric.minimize if metric.goal == thelper.optim.Metric.maximize \
                else thelper.optim.Metric.maximize
            self.logger.debug(f"will monitor metric '{self.monitor}' for best state checkpointing/early stopping")

        # parse checkpoint data from previous run (if available)
        ckptdata = {} if ckptdata is None else ckptdata
        self.monitor_best = thelper.utils.get_key_def("monitor_best", ckptdata, self.monitor_best)
        self.monitor_best_epoch = thelper.utils.get_key_def("monitor_best_epoch", ckptdata, -1)
        self.optimizer_state = thelper.utils.get_key_def("optimizer", ckptdata, None)
        self.scheduler_state = thelper.utils.get_key_def("scheduler", ckptdata, None)
        self.current_iter = thelper.utils.get_key_def("iter", ckptdata, 0)
        self.current_epoch = thelper.utils.get_key_def("epoch", ckptdata, 0)
        self.outputs = thelper.utils.get_key_def("outputs", ckptdata, {})

        # parse callbacks (see ``thelper.typedefs.IterCallbackType`` and ``thelper.typedefs.IterCallbackParams`` definitions)
        for cname, mset in zip(["train", "valid", "test"], [self.train_metrics, self.valid_metrics, self.test_metrics]):
            # parse user (custom) callback
            user_callback_keys = [f"{cname}_iter_callback", f"{cname}_callback", "callback"]
            user_callback = thelper.utils.get_key_def(user_callback_keys, trainer_config)  # type: Optional[typ.IterCallbackType]
            if user_callback is not None:
                assert f"{cname}_user_callback" not in mset, f"metrics set already had a '{cname}_user_callback' in it"
                mset[f"{cname}_user_callback"] = thelper.train.utils.PredictionCallback(user_callback)
            # parse display callback
            display_callback_keys = [f"display_{cname}_preds", f"display_{cname}_predictions", f"display_{cname}",
                                     "display_preds", "display_predictions", "display"]
            display_callback = thelper.utils.get_key_def(display_callback_keys, trainer_config)
            if display_callback:
                assert f"{cname}_display_callback" not in mset, f"metrics set already had a '{cname}_display_callback' in it"
                if isinstance(display_callback, bool):  # if simply toggled on, use default draw function wrapper
                    display_callback = {"type": "thelper.train.utils._draw_wrapper", "params": {"save": False}}
                mset[f"{cname}_display_callback"] = thelper.train.utils.PredictionCallback(display_callback)
            # parse logging callback
            logging_callback_keys = [f"{cname}_logger", f"{cname}_log", f"logger_{cname}", f"log_{cname}", "log", "logger"]
            logging_callback = thelper.utils.get_key_def(logging_callback_keys, trainer_config, self._iter_logger_callback)
            if logging_callback:
                assert f"{cname}_logger_callback" not in mset, f"metrics set already had a '{cname}_logger_callback' in it"
                logging_kwargs = {"set_name": cname, "writers": self.writers}  # pass writers by ref, will be filled later
                mset[f"{cname}_logger_callback"] = thelper.train.utils.PredictionCallback(logging_callback, logging_kwargs)
            else:
                logger.warning("logging is disabled by user, internal iteration count might never be updated")

        # parse visualization config (if any)
        self.viz = thelper.utils.get_key_def(["viz", "visualization", "visualizations"], trainer_config, {})
        assert isinstance(self.viz, dict), "invalid visulaization dictionary config"
        for viz_key, viz_config in self.viz.items():
            assert isinstance(viz_key, str) and viz_key in thelper.viz.supported_types, \
                f"invalid visualization type '{viz_key}' (not in available modules)"
            assert isinstance(viz_config, dict), f"invalid visualization configuration dictionary for type '{viz_key}'"

    def _init_writer(self, writer, path):
        if self.use_tbx and not writer:
            writer = self.tbx.SummaryWriter(path, comment=self.name)
            writer.add_text("config", json.dumps(self.config, indent=4, sort_keys=False, default=lambda x: str(x)))
            thelper.utils.save_config(self.config, os.path.join(path, "config.json"))
        return writer

    @staticmethod
    def _set_rng_state(seeds, epoch):
        if "torch" in seeds:
            torch.manual_seed(seeds["torch"] + epoch)
            torch.cuda.manual_seed_all(seeds["torch"] + epoch)
        if "numpy" in seeds:
            np.random.seed(seeds["numpy"] + epoch)
        if "random" in seeds:
            random.seed(seeds["random"] + epoch)

    @staticmethod
    def _upload_model(model, dev):
        """Uploads a model to a specific device, wrapping it in ``torch.nn.DataParallel`` if needed."""
        if isinstance(dev, list):
            if len(dev) == 0:
                return model.cpu()
            elif len(dev) == 1:
                return model.cuda(dev[0])
            else:
                return torch.nn.DataParallel(model, device_ids=dev).cuda(dev[0])
        else:
            return model.to(dev)

    @staticmethod
    def _move_tensor(tensor, dev, detach=False):
        """Uploads a tensor to a specific device."""
        if isinstance(tensor, (list, tuple)):
            return [Trainer._move_tensor(t, dev) for t in tensor]
        if isinstance(tensor, dict):
            return {k: Trainer._move_tensor(t, dev) for k, t in tensor.items()}
        if not isinstance(tensor, torch.Tensor):
            return tensor  # ignored (cannot upload)
        if isinstance(dev, list):
            if len(dev) == 0:
                out = tensor.cpu()
            else:
                # no reason to have multiple devices if not cuda-enabled GPUs
                out = tensor.cuda(dev[0])
        else:
            out = tensor.to(dev)
        return out.detach() if detach else out

    def _load_optimization(self, model, dev):
        """Instantiates and returns all optimization objects required for training the model."""
        config = self.optimization_config  # for abbrev only
        assert isinstance(config, dict), "optimization config should be provided as a dictionary"
        assert self.train_loader is not None and self.train_loader, "optimization only useful with training data"
        loss = None  # can be omitted if using custom trainer
        if "loss" in config:
            uploader = functools.partial(self._move_tensor, dev=dev)
            loss = thelper.optim.create_loss_fn(config["loss"], model, self.train_loader, uploader)
        optimizer = None  # can be omitted if using custom trainer
        if "optimizer" in config:
            optimizer = thelper.optim.create_optimizer(config["optimizer"], model)
        scheduler, scheduler_step_metric = None, None
        if "scheduler" in config and config["scheduler"]:  # can always be omitted
            scheduler, scheduler_step_metric = thelper.optim.create_scheduler(config["scheduler"], optimizer)
        return loss, optimizer, scheduler, scheduler_step_metric

    def _load_devices(self, devices_str=None):
        """Validates and returns the list of CUDA devices available on the system."""
        self.logger.debug("loading available devices")
        if devices_str is not None:
            devices = []
            available_cuda_devices = None
            assert isinstance(devices_str, (str, list)), "unexpected device string type"
            if isinstance(devices_str, str):
                assert devices_str, "cannot specify empty device name, use 'None' to auto-detect"
                devices_str = devices_str.split(",")
            elif isinstance(devices_str, list):
                assert devices_str, "cannot specify empty device list, use 'None' to auto-detect"
                assert all([isinstance(dev_str, str) for dev_str in devices_str]), "unexpected type in dev list"
            for dev_idx, dev_str in enumerate(devices_str):
                assert "cuda" in dev_str or dev_str == "cpu", \
                    f"unknown device type '{dev_str}' (expecting 'cpu' or 'cuda:X')"
                if dev_str == "cpu":
                    assert len(devices_str) == 1, "cannot combine cpu with other devices"
                    return []
                if dev_str == "cuda" or dev_str == "cuda:all":
                    assert len(devices_str) == 1, "must specify device index (e.g. 'cuda:0') if combining devices"
                    if available_cuda_devices is None:
                        available_cuda_devices = thelper.utils.get_available_cuda_devices()
                    assert available_cuda_devices, "could not find any available cuda devices"
                    return available_cuda_devices
                assert "cuda:" in dev_str, "expecting cuda device format to be 'cuda:X' (where X is device index)"
                cuda_dev_idx = int(dev_str.rsplit(":", 1)[-1])
                assert thelper.utils.test_cuda_device_availability(cuda_dev_idx), f"cuda device '{dev_str}' unavailable"
                devices.append(cuda_dev_idx)
            return devices
        else:
            return thelper.utils.get_available_cuda_devices()

    def train(self):
        """Starts the training process.

        This function will train the model until the required number of epochs is reached, and then evaluate it
        on the test data. The setup of loggers, tensorboard writers is done here, so is model improvement tracking
        via monitored metrics. However, the code related to loss computation and back propagation is implemented in
        a derived class via :func:`thelper.train.base.Trainer.train_epoch`.
        """
        assert self.train_loader, "missing training data, invalid loader!"
        assert not isinstance(self.model, torch.jit.ScriptModule), "current impl cannot train model traces"  # TODO
        self.logger.debug(f"uploading model to '{str(self.devices)}'...")
        model = self._upload_model(self.model, self.devices)
        loss, optimizer, scheduler, scheduler_step_metric = self._load_optimization(model, self.devices)
        if optimizer is not None and self.optimizer_state is not None:
            optimizer.load_state_dict(self.optimizer_state)
            self.optimizer_state = None
        if scheduler is not None and self.scheduler_state is not None:
            scheduler.load_state_dict(self.scheduler_state)
            self.scheduler_state = None
        self.logger.info(f"loss: {str(loss)}")
        self.logger.info(f"optimizer: {str(optimizer)}")
        latest_loss = math.inf
        while self.current_epoch < self.epochs:
            self.writers["train"] = self._init_writer(self.writers["train"], self.output_paths["train"])
            self.logger.info(f"at epoch#{self.current_epoch} for '{self.name}' (dev={str(self.devices)})")
            if scheduler:
                if scheduler_step_metric:
                    if scheduler_step_metric == "loss":
                        # todo: use validation loss instead? more stable?
                        scheduler.step(metrics=latest_loss, epoch=self.current_epoch)
                    else:
                        metric = None
                        if self.valid_loader and scheduler_step_metric in self.valid_metrics:
                            metric = self.valid_metrics[scheduler_step_metric]
                        elif self.train_loader and scheduler_step_metric in self.train_metrics:
                            metric = self.train_metrics[scheduler_step_metric]
                        # note: makes no sense to look for it in test metrics
                        assert metric is not None, f"cannot find metric '{scheduler_step_metric}' for scheduler step"
                        assert isinstance(metric, thelper.optim.metrics.Metric), "monitoring consumer must be metric"
                        metric_anti_goal = thelper.optim.Metric.maximize \
                            if metric.goal == thelper.optim.Metric.minimize \
                            else thelper.optim.Metric.minimize
                        metric_val = metric.eval() if self.current_epoch > 0 else metric_anti_goal
                        scheduler.step(metrics=metric_val, epoch=self.current_epoch)
                else:
                    scheduler.step(epoch=self.current_epoch)
            if self.writers["train"] and not self.skip_tbx_histograms and \
                    (self.current_epoch % self.tbx_histogram_freq) == 0:
                for pname, param in model.named_parameters():
                    if "bn" in pname:
                        continue  # skip batch norm modules
                    pname = pname.replace(".", "/")  # for proper grouping
                    if pname.startswith("module/"):
                        pname = pname.replace("module/", "", 1)
                    if pname.startswith("model/"):
                        pname = pname.replace("model/", "", 1)
                    data = param.data.cpu().numpy().flatten()
                    self.writers["train"].add_histogram(pname, data, self.current_epoch)
                    if param.grad is not None:
                        grad = param.grad.data.cpu().numpy().flatten()
                        self.writers["train"].add_histogram(pname + '/grad', grad, self.current_epoch)
            self.logger.debug(f"learning rate at {thelper.optim.get_lr(optimizer):.8f}")
            self._set_rng_state(self.train_loader.seeds, self.current_epoch)
            model.train()
            if hasattr(self.train_loader, "set_epoch") and callable(self.train_loader.set_epoch):
                self.train_loader.set_epoch(self.current_epoch)
            latest_loss = self.train_epoch(model, self.current_epoch, self.devices, loss, optimizer,
                                           self.train_loader, self.train_metrics, self.output_paths["train"])
            self._write_epoch_output(self.current_epoch, self.train_metrics,
                                     self.writers["train"], self.output_paths["train"],
                                     loss=latest_loss, optimizer=optimizer)
            train_metric_vals = {metric_name: metric.eval() for metric_name, metric in self.train_metrics.items()
                                 if isinstance(metric, thelper.optim.metrics.Metric)}
            result = {"train/loss": latest_loss, "train/metrics": train_metric_vals}
            monitor_type_key = "train/metrics"  # if we cannot run validation, will monitor progression on training metrics
            if self.valid_loader:
                self._set_rng_state(self.valid_loader.seeds, self.current_epoch)
                model.eval()
                self.writers["valid"] = self._init_writer(self.writers["valid"], self.output_paths["valid"])
                for metric in self.valid_metrics.values():
                    metric.reset()  # force reset here, we always evaluate from a clean state
                if hasattr(self.valid_loader, "set_epoch") and callable(self.valid_loader.set_epoch):
                    self.valid_loader.set_epoch(self.current_epoch)
                self.eval_epoch(model, self.current_epoch, self.devices, self.valid_loader,
                                self.valid_metrics, self.output_paths["valid"])
                self._write_epoch_output(self.current_epoch, self.valid_metrics,
                                         self.writers["valid"], self.output_paths["valid"])
                valid_metric_vals = {metric_name: metric.eval() for metric_name, metric in self.valid_metrics.items()
                                     if isinstance(metric, thelper.optim.metrics.Metric)}
                result = {**result, "valid/metrics": valid_metric_vals}
                monitor_type_key = "valid/metrics"  # since validation is available, use that to monitor progression
                uploader = functools.partial(self._move_tensor, dev=self.devices, detach=True)
                wrapped_loader = thelper.data.DataLoaderWrapper(self.valid_loader, uploader)
                for viz, kwargs in self.viz.items():
                    viz_img = thelper.viz.visualize(model, self.task, wrapped_loader, viz_type=viz, **kwargs)
                    if viz_img is not None:
                        if self.writers["valid"] is not None:
                            self.writers["valid"].add_image(f"viz/{viz}", viz_img, self.current_epoch, dataformats="HWC")
                        raw_filepath = os.path.join(self.output_paths["valid"], f"{viz}-{self.current_epoch:04d}.png")
                        self.logger.debug(f"writing {viz} render output to {os.path.abspath(raw_filepath)}")
                        cv.imwrite(raw_filepath, viz_img[..., ::-1])
            new_best = False
            monitor_val = None
            for key, value in result.items():
                if key == monitor_type_key and self.monitor is not None:
                    assert self.monitor in value, f"not monitoring required variable '{self.monitor}' in metrics"
                    monitor_val = value[self.monitor]
                    if (self.monitor_goal == thelper.optim.Metric.minimize and monitor_val < self.monitor_best) or \
                       (self.monitor_goal == thelper.optim.Metric.maximize and monitor_val > self.monitor_best):
                        self.monitor_best = monitor_val
                        self.monitor_best_epoch = self.current_epoch
                        new_best = True
                if not isinstance(value, dict):
                    self.logger.info(f" epoch#{self.current_epoch} result =>  {str(key)}: {value}")
                else:
                    for subkey, subvalue in value.items():
                        self.logger.info(f" epoch#{self.current_epoch} result =>  {str(key)}:{str(subkey)}: {subvalue}")
            if self.monitor is not None:
                assert monitor_val is not None, f"training/validation did not evaluate required metric '{self.monitor}'"
                if new_best:
                    best_str = "(new best value)"
                else:
                    best_str = f"(previous best = {self.monitor_best} @ epoch = {self.monitor_best_epoch})"
                self.logger.info(f"epoch {self.current_epoch}, monitored {self.monitor} = {monitor_val}  {best_str}")
            self.outputs[self.current_epoch] = result
            if new_best or (self.current_epoch % self.save_freq) == 0:
                self.logger.info(f"saving checkpoint @ epoch#{self.current_epoch}")
                self._save(self.current_epoch, self.current_iter, optimizer, scheduler, save_best=new_best)
            self.current_epoch += 1
        self.logger.info(f"training for session '{self.name}' done")
        return self.outputs

    def eval(self):
        """Starts the evaluation process.

        This function will evaluate the model using the test data (or the validation data, if no test data is available),
        and return the results. Note that the code related to the forwarding of samples inside the model itself is implemented
        in a derived class via :func:`thelper.train.base.Trainer.eval_epoch`.
        """
        assert self.valid_loader or self.test_loader, "missing validation/test data, invalid loaders!"
        self.logger.debug(f"uploading model to '{str(self.devices)}'...")
        model = self._upload_model(self.model, self.devices)
        result = {}
        output_group = None, None
        if self.test_loader:
            self._set_rng_state(self.test_loader.seeds, self.current_epoch)
            model.eval()
            self.writers["test"] = self._init_writer(self.writers["test"], self.output_paths["test"])
            for metric in self.test_metrics.values():
                metric.reset()  # force reset here, we always evaluate from a clean state
            if hasattr(self.test_loader, "set_epoch") and callable(self.test_loader.set_epoch):
                self.test_loader.set_epoch(self.current_epoch)
            self.eval_epoch(model, self.current_epoch, self.devices, self.test_loader,
                            self.test_metrics, self.output_paths["test"])
            self._write_epoch_output(self.current_epoch, self.test_metrics,
                                     self.writers["test"], self.output_paths["test"], use_suffix=False)
            test_metric_vals = {metric_name: metric.eval() for metric_name, metric in self.test_metrics.items()
                                if isinstance(metric, thelper.optim.metrics.Metric)}
            result = {**result, **test_metric_vals}
            output_group = "test/metrics"
            uploader = functools.partial(self._move_tensor, dev=self.devices, detach=True)
            wrapped_loader = thelper.data.DataLoaderWrapper(self.test_loader, uploader)
            for viz, kwargs in self.viz.items():
                viz_img = thelper.viz.visualize(model, self.task, wrapped_loader, viz_type=viz, **kwargs)
                if viz_img is not None:
                    if self.writers["test"] is not None:
                        self.writers["test"].add_image(f"viz/{viz}", viz_img, self.current_epoch, dataformats="HWC")
                    raw_filepath = os.path.join(self.output_paths["test"], f"{viz}-{self.current_epoch:04d}.png")
                    self.logger.debug(f"writing {viz} render output to {os.path.abspath(raw_filepath)}")
                    cv.imwrite(raw_filepath, viz_img[..., ::-1])
        elif self.valid_loader:
            self._set_rng_state(self.valid_loader.seeds, self.current_epoch)
            model.eval()
            self.writers["valid"] = self._init_writer(self.writers["valid"], self.output_paths["valid"])
            for metric in self.valid_metrics.values():
                metric.reset()  # force reset here, we always evaluate from a clean state
            if hasattr(self.valid_loader, "set_epoch") and callable(self.valid_loader.set_epoch):
                self.valid_loader.set_epoch(self.current_epoch)
            self.eval_epoch(model, self.current_epoch, self.devices, self.valid_loader,
                            self.valid_metrics, self.output_paths["valid"])
            self._write_epoch_output(self.current_epoch, self.valid_metrics,
                                     self.writers["valid"], self.output_paths["valid"], use_suffix=False)
            valid_metric_vals = {metric_name: metric.eval() for metric_name, metric in self.valid_metrics.items()
                                 if isinstance(metric, thelper.optim.metrics.Metric)}
            result = {**result, **valid_metric_vals}
            output_group = "valid/metrics"
            uploader = functools.partial(self._move_tensor, dev=self.devices, detach=True)
            wrapped_loader = thelper.data.DataLoaderWrapper(self.valid_loader, uploader)
            for viz, kwargs in self.viz.items():
                viz_img = thelper.viz.visualize(model, self.task, wrapped_loader, viz_type=viz, **kwargs)
                if viz_img is not None:
                    if self.writers["valid"] is not None:
                        self.writers["valid"].add_image(f"viz/{viz}", viz_img, self.current_epoch, dataformats="HWC")
                    raw_filepath = os.path.join(self.output_paths["valid"], f"{viz}-{self.current_epoch:04d}.png")
                    self.logger.debug(f"writing {viz} render output to {os.path.abspath(raw_filepath)}")
                    cv.imwrite(raw_filepath, viz_img[..., ::-1])
        for key, value in result.items():
            if not isinstance(value, dict):
                self.logger.info(f" final result =>  {str(key)}: {value}")
            else:
                for subkey, subvalue in value.items():
                    self.logger.info(f" final result =>  {str(key)}:{str(subkey)}: {subvalue}")
        if self.current_epoch not in self.outputs:
            # probably using an 'untrained model' (such as a FCN adapted from a classifier)
            self.outputs[self.current_epoch] = {}
        self.outputs[self.current_epoch][output_group] = result
        self.logger.info(f"evaluation for session '{self.name}' done")
        return self.outputs

    @abstractmethod
    def train_epoch(self, model, epoch, dev, loss, optimizer, loader, metrics, output_path):
        """Trains the model for a single epoch using the provided objects.

        Args:
            model: the model to train that is already uploaded to the target device(s).
            epoch: the epoch index we are training for (0-based).
            dev: the target device that tensors should be uploaded to.
            loss: the loss function used to evaluate model fidelity.
            optimizer: the optimizer used for back propagation.
            loader: the data loader used to get transformed training samples.
            metrics: the dictionary of metrics/consumers to update every iteration.
            output_path: directory where output files should be written, if necessary.
        """
        raise NotImplementedError

    @abstractmethod
    def eval_epoch(self, model, epoch, dev, loader, metrics, output_path):
        """Evaluates the model using the provided objects.

        Args:
            model: the model to evaluate that is already uploaded to the target device(s).
            epoch: the epoch index we are training for (0-based).
            dev: the target device that tensors should be uploaded to.
            loader: the data loader used to get transformed valid/test samples.
            metrics: the dictionary of metrics/consumers to update every iteration.
            output_path: directory where output files should be written, if necessary.
        """
        raise NotImplementedError

    def _to_tensor(self, sample):
        """Fetches and returns tensors of input and groundtruth data from a batched sample dictionary.

        The specifics of how to unpack a sample dictionary into usable parts is tied to the trainer, so
        it cannot be defined in a perfectly generic way here. The implementation below is given as a
        baseline to support some visualization techniques (see :mod:`thelper.viz` for more info). Derived
        trainers (both custom and framework-provided) are likely to override this function to properly
        unpack groundtruth data.

        Args:
            sample: the (batched) sample to unpack into tensors, obtained directly from a data loader.

        Returns:
            A tuple of input data and groundtruth data tensors. In this implementation, the groundtruth
            data tensor is always ``None``.
        """
        assert isinstance(sample, dict), "trainer expects samples to come in dicts for key-based usage"
        assert self.task.input_key in sample, f"could not find input key '{self.task.input_key}' in sample dict"
        return torch.FloatTensor(sample[self.task.input_key]), None

    # noinspection PyUnusedLocal
    def _iter_logger_callback(self,         # see `thelper.typedefs.IterCallbackParams` for more info
                              task,         # type: thelper.tasks.utils.Task
                              input,        # type: thelper.typedefs.InputType
                              pred,         # type: thelper.typedefs.AnyPredictionType
                              target,       # type: thelper.typedefs.AnyTargetType
                              sample,       # type: thelper.typedefs.SampleType
                              loss,         # type: Optional[float]
                              iter_idx,     # type: int
                              max_iters,    # type: int
                              epoch_idx,    # type: int
                              max_epochs,   # type: int
                              output_path,  # type: AnyStr
                              # note: kwargs must contain two args here: 'set_name' and 'writers'
                              **kwargs,     # type: Any
                              ):            # type: (...) -> None
        """Receives callback data for logging loss/monitored metric values each training/eval iteration."""
        # NOTE: THIS FUNCTION IS RESPONSIBLE FOR INCREASING THE INTERNAL ITERATION COUNTER.
        set_name = thelper.utils.get_key("set_name", kwargs, "missing set name in iter logger args")
        assert set_name in ["train", "valid", "test"], "unrecognized iter logger set name"
        metrics = self.train_metrics if set_name == "train" else self.valid_metrics if set_name == "valid" \
            else self.test_metrics
        monitor_val = None
        monitor_str = ""
        if self.monitor is not None and self.monitor in metrics:
            assert isinstance(metrics[self.monitor], thelper.optim.metrics.Metric), "unexpected metric type"
            if metrics[self.monitor].live_eval:
                monitor_val = metrics[self.monitor].eval()
                monitor_str = f"   {self.monitor}: {monitor_val:.2f}"
        loss_str = ""
        if loss is not None:
            loss_str = f"   loss: {loss:.6f}"
        assert self.current_epoch == epoch_idx, "something's messed up"
        self.logger.info(
            f"{set_name} epoch#{epoch_idx}  (iter#{self.current_iter})" +
            f"   batch: {iter_idx + 1}/{max_iters} ({((iter_idx + 1) / max_iters) * 100.0:.0f}%)" +
            f"{loss_str}{monitor_str}"
        )
        writers = thelper.utils.get_key("writers", kwargs, msg="missing writers dict in iter logger args")
        if (set_name == "train" or iter_idx == max_iters - 1) and writers[set_name]:
            if loss is not None:
                writers[set_name].add_scalar("iter/loss", loss, self.current_iter)
            for metric_name, metric in metrics.items():
                if isinstance(metric, thelper.optim.metrics.Metric):
                    if metric_name == self.monitor and monitor_val is not None:
                        writers[set_name].add_scalar(f"iter/{self.monitor}", monitor_val, self.current_iter)
                    elif metric.live_eval:
                        # if live eval is not true, metric might be too heavy to compute at each iteration
                        writers[set_name].add_scalar(f"iter/{metric_name}", metric.eval(), self.current_iter)
        if set_name == "train":
            self.current_iter += 1

    def _write_epoch_output(self, epoch, metrics, tbx_writer, output_path, loss=None, optimizer=None, use_suffix=True):
        """Writes the cumulative evaluation result of all metrics using a specific writer."""
        self.logger.debug(f"writing epoch metrics to {os.path.abspath(output_path)}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if tbx_writer is not None and loss is not None and optimizer is not None:
            tbx_writer.add_scalar("epoch/loss", loss, epoch)
            tbx_writer.add_scalar("epoch/lr", thelper.optim.get_lr(optimizer), epoch)
        for metric_name, metric in metrics.items():
            if isinstance(metric, thelper.optim.metrics.Metric) and tbx_writer is not None:
                tbx_writer.add_scalar(f"epoch/{metric_name}", metric.eval(), epoch)
            if hasattr(metric, "render") and callable(metric.render):
                img = metric.render()
                if img is not None:
                    if tbx_writer is not None:
                        tbx_writer.add_image(metric_name, img, epoch, dataformats="HWC")
                    raw_filename = f"{metric_name}{f'-{epoch:04d}' if use_suffix else ''}.png"
                    raw_filepath = os.path.join(output_path, raw_filename)
                    self.logger.debug(f"writing metric render output to {os.path.abspath(raw_filepath)}")
                    cv.imwrite(raw_filepath, img[..., [2, 1, 0]])
            txt = metric.report() if hasattr(metric, "report") and callable(metric.report) else None
            ext = getattr(metric, "ext", "txt")
            if not txt and isinstance(metric, thelper.optim.metrics.Metric):
                eval_res = metric.eval()
                if eval_res is not None:
                    if isinstance(eval_res, float):
                        txt = f"{eval_res:.4f}"  # make sure we always have decent precision
                    else:
                        txt = str(eval_res)
            if txt:
                raw_filename = f"{metric_name}{f'-{epoch:04d}' if use_suffix else ''}.{ext}"
                raw_filepath = os.path.join(output_path, raw_filename)
                self.logger.debug(f"writing metric text output to '{os.path.abspath(raw_filepath)}'")
                with open(raw_filepath, "w") as fd:
                    fd.write(txt)

    def _save(self, epoch, iter, optimizer, scheduler, save_best=False):
        """Saves a session checkpoint containing all the information required to resume training."""
        # logically, this should only be called during training (i.e. with a valid optimizer)
        log_stamp = thelper.utils.get_log_stamp()
        # the saved state below should be kept compatible with the one in thelper.cli.export_model
        curr_state = {
            "name": self.name,
            "epoch": epoch,
            "iter": iter,
            "source": log_stamp,
            "git_sha1": thelper.utils.get_git_stamp(),
            "version": thelper.__version__,
            "task": str(self.task) if self.save_raw else self.task,
            "outputs": self.outputs,
            # we save model type/params here in case those are not in the current config
            "model": self.model.state_dict() if self.save_raw else self.model,
            "model_type": self.model.get_name(),
            "model_params": self.model.config if self.model.config else {},
            "optimizer": optimizer.state_dict() if optimizer is not None else None,
            "scheduler": scheduler.state_dict() if (scheduler is not None and
                                                    hasattr(scheduler, "state_dict")) else None,
            "monitor_best": self.monitor_best,
            "monitor_best_epoch": self.monitor_best_epoch,
            "config": self.config  # note: this is the global app config
        }
        filename = f"ckpt.{epoch:04d}.{log_stamp}.pth"
        filename = os.path.join(self.checkpoint_dir, filename)
        self.logger.debug(f"writing checkpoint to {os.path.abspath(filename)}")
        torch.save(curr_state, filename)
        if save_best:
            filename_best = os.path.join(self.checkpoint_dir, "ckpt.best.pth")
            self.logger.debug(f"writing checkpoint to {os.path.abspath(filename_best)}")
            torch.save(curr_state, filename_best)
