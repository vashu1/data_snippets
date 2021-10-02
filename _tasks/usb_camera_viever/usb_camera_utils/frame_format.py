import logging

# select format == DEFAULT_SCREEN_SIZE if there is one, otherwise pick 1st one
def select_frame_format(frame_formats, DEFAULT_SCREEN_SIZE):
    frmt2str = lambda frmt: str(frmt).replace('uvc_frame_format.', '')
    print('Available frame formats:')
    print('\n'.join([frmt2str(i) for i in frame_formats]))
    for frame_format in frame_formats:
        width, height = DEFAULT_SCREEN_SIZE
        if frame_format['width'] == width and frame_format['height'] == height:
            print(f'\nSelected: {frmt2str(frame_format)}\n')
            return frame_format
    if frame_formats:
        print(f'\nSelected: {frmt2str(frame_formats[0])}\n')
        return frame_formats[0]
    else:
        logging.error('libuvc cannot access frame format for device!')
        exit(1)