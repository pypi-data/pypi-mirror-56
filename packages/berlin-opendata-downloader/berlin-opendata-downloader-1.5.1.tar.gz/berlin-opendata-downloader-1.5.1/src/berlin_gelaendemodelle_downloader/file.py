import re
import os

from pandas import DataFrame

from .utils import data_frame_2_file_content, file_content_2_data_frame, data_frame_2_geo_data_frame
from .constant import ORIGNAL_SUB_PATH, COMPRESSED_SUB_PATH, TXT_FILE_FORMAT, GEOJSON_FILE_FORMAT, CSV_FILE_FORMAT



def write_file_content_as_txt(download_path: str, file_name: str, file_content: list) ->  None:
    """
    Writes the given ``file_content`` to the given path as txt file.

    Args:
        download_path (str): directory
        file_name (str): file name
        file_content (list): list of lines for serialization as file
    """

    compression_directory = os.path.splitext(file_name)[1][1:].lower()

    with open(os.path.join(download_path, compression_directory, file_name), mode="w") as file:
        file.writelines("\n".join(file_content))


def save_files(download_path: str, file_name: str, original_content: str, data_frame: DataFrame, file_formats: tuple, keep_original: bool) -> None:
    """
    Saves all files that are downloaded or created to the proper directories.

    Args:
        download_path (str): Path to the download directory.
        file_name (str): file name.
        original_content (str): Original download content.
        data_frame (DataFrame): If data were compressed, the corresponding compressed ``DataFrame`` or ``GeoDataFrame``.
        file_formats (tuple): Formats to save.
        keep_original (bool): Flag that indicates whether to save the original files.
    """

    original_path   = os.path.join(download_path, ORIGNAL_SUB_PATH)
    compressed_path = os.path.join(download_path, COMPRESSED_SUB_PATH)

    if keep_original:
        if TXT_FILE_FORMAT in file_formats:
            write_file_content_as_txt(original_path, file_name, original_content)
        
        if GEOJSON_FILE_FORMAT in file_formats:
            geo_df = data_frame_2_geo_data_frame(file_content_2_data_frame(original_content))
            geo_df.to_file(os.path.join(original_path, "geojson", f"{os.path.splitext(file_name)[0]}.geojson"), driver='GeoJSON')

        if CSV_FILE_FORMAT in file_formats:
            df = file_content_2_data_frame(original_content)
            df[["x", "y", "height"]].to_csv(os.path.join(original_path, "csv", f"{os.path.splitext(file_name)[0]}.csv"), index=False)

    if data_frame is not None:
        if TXT_FILE_FORMAT in file_formats:
            file_content_compressed = data_frame_2_file_content(data_frame)
            write_file_content_as_txt(compressed_path, file_name, file_content_compressed)

        if GEOJSON_FILE_FORMAT in file_formats:
            data_frame.to_file(os.path.join(compressed_path, "geojson", f"{os.path.splitext(file_name)[0]}.geojson"), driver='GeoJSON')

        if CSV_FILE_FORMAT in file_formats:
            data_frame[["x", "y", "height"]].to_csv(os.path.join(compressed_path, "csv", f"{os.path.splitext(file_name)[0]}.csv"), index=False)
