import os
import pytest
from flight_monitor import load_data, save_data

def test_load_and_save_data(tmp_path, monkeypatch):
    # Usando o monkeypatch para mudar o DATA_FILE para um arquivo temporário durante o teste
    temp_file = tmp_path / "test_data.json"
    monkeypatch.setattr("flight_monitor.DATA_FILE", str(temp_file))
    
    # Testa salvar dados
    test_data = {"history": [], "last_average": 1500.0}
    save_data(test_data)
    
    assert os.path.exists(temp_file)
    
    # Testa carregar dados
    loaded_data = load_data()
    assert loaded_data["last_average"] == 1500.0

def test_load_data_no_file(tmp_path, monkeypatch):
    # Testa o comportamento quando o arquivo não existe
    temp_file = tmp_path / "non_existent_data.json"
    monkeypatch.setattr("flight_monitor.DATA_FILE", str(temp_file))
    
    loaded_data = load_data()
    assert loaded_data == {"history": [], "last_average": None}
