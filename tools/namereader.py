import sys
import os

fn = open('name.csv', 'r')
sheet = fn.readlines()
fn.close()


print sheet[0].split()
