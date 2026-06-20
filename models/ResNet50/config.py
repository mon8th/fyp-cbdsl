DATA_DIR = 'data'

TRAIN_DIR = DATA_DIR + '/split_grouped/train'
VAL_DIR   = DATA_DIR + '/split_grouped/val'
TEST_DIR  = DATA_DIR + '/split_grouped/test'

NUM_CLASSES = 50

IMAGE_SIZE = 224
BATCH_SIZE = 32

NUM_EPOCHS    = 50
FREEZE_EPOCHS = 5

FREEZE_LR   = 1e-3
FINETUNE_LR = 1e-4

WEIGHT_DECAY    = 2e-5
LABEL_SMOOTHING = 0.1

SEED        = 42
NUM_WORKERS = 4
PIN_MEMORY  = True

CHECKPOINT_DIR  = 'checkpoints'
BEST_MODEL_PATH = CHECKPOINT_DIR + '/best_resnet50.pth'