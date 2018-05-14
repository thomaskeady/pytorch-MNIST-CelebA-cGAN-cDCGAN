from CustomDataset import CustomDataset
import torch

test = CustomDataset('data/processed/cedict_vectors_v2.csv', 'data/processed/cedict_dir_v2/', '.png')

train_loader = torch.utils.data.DataLoader(test, batch_size=128, shuffle=True)

for x, y in train_loader:
	print(str(y))

