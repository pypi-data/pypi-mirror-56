import click

from tqdm import tqdm

from .file import save_files
from .download import get_subset_links, download_zip
from .utils import file_content_2_data_frame, create_directories, compress_data_frame, data_frame_2_geo_data_frame
from .constant import COMPRESS_HELP, KEEP_ORIGIGNAL_HELP, COMPRESS_DEFAULT, SUPPORTED_FILE_FORMATS_DEFAULT, SUPPORTED_FILE_FORMATS_HELP, SUPPORTED_FILE_FORMATS_CHOICE, GEOJSON_FILE_FORMAT



@click.group()
def cli():
    """
    Entrypoint of CLI implementation.
    """


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("download-path", type=click.Path(exists=True, dir_okay=True, writable=True))
@click.option("--keep-original", type=bool, is_flag=True, help=KEEP_ORIGIGNAL_HELP)
@click.option("--compress", type=int, default=COMPRESS_DEFAULT, help=COMPRESS_HELP)
@click.option("--file-format", type=click.Choice(SUPPORTED_FILE_FORMATS_CHOICE, case_sensitive=True), default=SUPPORTED_FILE_FORMATS_DEFAULT, help=SUPPORTED_FILE_FORMATS_HELP, multiple=True)
def download(download_path: str, keep_original: bool, compress: int, file_format: tuple):
    """
    Downloads height information of Berlin to DOWNLOAD-PATH.
    """

    # Set constraints
    if compress <= 0:
        keep_original = True

    # creats all necessary directories
    original_path, compressed_path = create_directories(download_path, keep_original, compress, file_format)
    links = get_subset_links()

    # Without compression: download and keep the original files.
    if compress <= 0:
        for link in tqdm(links):

            file_name, file_content = download_zip(link)
            save_files(download_path, file_name, file_content, None, file_format, keep_original)


    # With compression: download and compress the data. Only save the originals it ``--keep-original`` is set.
    elif 2000 % compress == 0:
        for link in tqdm(links):

            file_name, file_content = download_zip(link)

            data_frame = file_content_2_data_frame(file_content)
            compressed_data_frame = compress_data_frame(data_frame, compress)

            if GEOJSON_FILE_FORMAT in file_format:
                compressed_data_frame = data_frame_2_geo_data_frame(compressed_data_frame)

            save_files(download_path, file_name, file_content, compressed_data_frame, file_format, keep_original)

    else:
        raise click.BadParameter("Argument 'compress' have to divide 2000 without remainder.")
