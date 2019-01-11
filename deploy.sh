#!/bin/bash

pip install --upgrade  .
jupyter nbextension install cq_jupyter --user
jupyter nbextension enable cq_jupyter/js/main --user
jupyter-nbextension list
