batch_size = 10
training_steps = 10
steps_per_epoch = 2
epochs_per_eval = 3
training_epochs = int(training_steps // steps_per_epoch)

cpu_cores = 8
multi_gpu = True
shuffle_buffer = batch_size * cpu_cores
# ########################
# Load VeRi dataset
# ########################
veri_dataset = faceid.dataset.VeRiDataset(root_dir=args.dataset_dir).load()

# ########################
# Define a Classifier
# ########################
estimator = tf.estimator.Estimator(
    model_fn=faceid.resnet_carid(multi_gpu=multi_gpu),
    model_dir=args.model_dir,
    config=tf.estimator.RunConfig().replace(
        save_checkpoints_steps=steps_per_epoch,
        save_summary_steps=steps_per_epoch,
        log_step_count_steps=steps_per_epoch),
    params={
        'learning_rate': 0.001,
        'weight_decay': 2e-4,
        'optimizer': tf.train.AdamOptimizer,
        'multi_gpu': multi_gpu,
        'loss_function': faceid.triplet_loss,
        'margin': 0.2
    })

# #########################
# Training/Eval
# #########################
tensors_to_log = ['train_loss']
for _ in range(training_epochs // epochs_per_eval):
    train_data, eval_data = veri_dataset.split_training_data(
        test_size=0.2,
        shuffle=True)

    estimator.train(
        input_fn=lambda: veri_dataset.get_input_fn(
            mode=tf.estimator.ModeKeys.TRAIN,
            dataset=train_data,  # pylint: disable=cell-var-from-loop
            batch_size=batch_size,
            parse_fn=_read_py_function,
            shuffle_buffer=shuffle_buffer,
            num_parallel_calls=cpu_cores),
        steps=steps_per_epoch * epochs_per_eval,
        hooks=[faceid.ProgressBarHook(
            epochs=int(training_steps // steps_per_epoch),
            steps_per_epoch=steps_per_epoch,
            tensors_to_log=tensors_to_log)])

    print("\nStart evaluating...")
    eval_result = estimator.evaluate(
        input_fn=lambda: veri_dataset.get_input_fn(
            mode=tf.estimator.ModeKeys.EVAL,
            dataset=eval_data,  # pylint: disable=cell-var-from-loop
            batch_size=batch_size,
            parse_fn=_read_py_function,
            shuffle_buffer=None,
            num_parallel_calls=cpu_cores),
        steps=200)
    print(eval_result)
print("---- Training Completed ----")