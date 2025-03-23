from loguru import logger
import general.base_utils as general
from lyricsgenius import Genius

def init_genius():
    envs = general.init_env_variables('GENIUS_ACCESS_TOKEN')
    return Genius(envs['GENIUS_ACCESS_TOKEN'], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

def main():
    global GENIUS_INSTANCE, CLICKHOUSE_INSTANCE
    GENIUS_INSTANCE = init_genius()
    CLICKHOUSE_INSTANCE = general.init_clickhouse()
       
if __name__ == "__main__":
    main()