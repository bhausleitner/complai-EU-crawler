from click.testing import CliRunner

from regulatory_data_collection.eur_lex_webservice import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
