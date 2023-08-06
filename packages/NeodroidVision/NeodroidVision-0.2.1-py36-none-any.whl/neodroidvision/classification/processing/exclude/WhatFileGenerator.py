#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from torchvision import datasets, transforms

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 10/11/2019
           '''


def FileGenerator(batch_size=16,
                  workers=1,
                  path='/home/heider/Data/Datasets/Vision/vestas'):
  a_transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor()
    ])

  a_retransform = transforms.Compose([
    transforms.ToPILImage('RGB')
    ])

  train_dataset = datasets.ImageFolder(path, a_transform)

  if False:
    train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
  else:
    train_sampler = None

  torch.manual_seed(time.time())
  train_loader = torch.utils.data.DataLoader(train_dataset,
                                             batch_size=batch_size,
                                             shuffle=(train_sampler is None),
                                             num_workers=workers,
                                             pin_memory=True,
                                             sampler=train_sampler)


if __name__ == '__main__':
  LATEST_GPU_STATS = FileGenerator()
  for i, (g, c) in enumerate(LATEST_GPU_STATS):
    print(c)
