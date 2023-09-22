CLASSES = ('airplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
           'cat', 'chair', 'cow', 'dining table', 'dog', 'horse', 'motorcycle',
           'person', 'potted plant', 'sheep', 'couch', 'train', 'tv')

dataset_type = 'CocoDataset'
data_root = 'data/VOC_0712_converted/'

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(1000, 600), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1000, 600),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=4,
    workers_per_gpu=8,
    train=dict(
        type='RepeatDataset',
        times=3,
        dataset=dict(
            type=dataset_type,
            ann_file=data_root + 'voc0712_train_all.json',
            img_prefix=data_root + 'JPEGImages',
            pipeline=train_pipeline,
            classes=CLASSES)),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'val_coco_format.json',
        img_prefix=data_root + 'JPEGImages',
        pipeline=test_pipeline,
        classes=CLASSES),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'val_coco_format.json',
        img_prefix=data_root + 'JPEGImages',
        pipeline=test_pipeline,
        classes=CLASSES))
evaluation = dict(interval=1, metric='bbox')
