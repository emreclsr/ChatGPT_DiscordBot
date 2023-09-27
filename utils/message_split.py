import re
from loguru import logger


def message_split(message: str):
    logger.info("Message split start")
    # Split the response while preserving code blocks
    code_blocks = re.split(r'```(.*?)```', message, flags=re.DOTALL)
    message_chunks = []

    # Every second message is a code block
    for i in range(len(code_blocks) // 2):
        message_chunks.append(code_blocks[i * 2])
        message_chunks.append(f'```{code_blocks[i * 2 + 1]}\n```')

    # Add the remaining text
    if len(code_blocks) % 2 == 1:
        message_chunks.append(code_blocks[-1])

    logger.info(f"Message split {len(message_chunks)} parts.")
    return message_chunks
