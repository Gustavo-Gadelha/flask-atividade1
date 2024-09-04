from pathlib import Path

from dotenv import load_dotenv

from app import create_app

env_path: Path = Path(__file__).parent / '.env'

if env_path.exists():
    load_dotenv(env_path)

app = create_app('development')



if __name__ == '__main__':
    app.run()
