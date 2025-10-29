import streamlit as st
import pandas as pd
import matplotlib as m
import numpy as n
from google.cloud import speech_v2 as speech

from controller.controller import Controller
from view.view import View

def main():
    controller = Controller()
    view = View(controller)

    view.display()

if __name__ == "__main__":
    main()