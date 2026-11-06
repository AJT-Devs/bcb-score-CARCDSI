"""Configuração central de logging."""

import logging


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)