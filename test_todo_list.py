from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
import time

# # Configurar o WebDriver (usando webdriver_manager para gerenciar o download do ChromeDriver)
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

# Abrir o arquivo HTML local
driver.get("file:///C:/Users/Win10/Desktop/Senac/Sem5/Qualidade%20de%20Software/Gincana3/teste01/code/index.html")

# Função de teste
def test_todo_list():
    try:
        # Verificar se a lista de tarefas está vazia
        task_list = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "task-list"))
        )
        tasks = task_list.find_elements(By.TAG_NAME, 'li')
        assert len(tasks) == 0, "A lista de tarefas deve começar vazia."

        # Encontrar o campo de entrada de nova tarefa
        new_task_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "new-task"))
        )

        # Adicionar uma nova tarefa
        new_task_input.send_keys('Teste tarefa 1')
        new_task_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

        # Verificar se a nova tarefa foi adicionada
        tasks = task_list.find_elements(By.TAG_NAME, 'li')
        assert len(tasks) == 1, "A tarefa não foi adicionada corretamente."
        assert tasks[0].find_element(By.TAG_NAME, 'span').text == 'Teste tarefa 1', "O texto da tarefa não está correto."

        # Marcar a tarefa como concluída
        check_button = tasks[0].find_element(By.CLASS_NAME, 'check-btn')
        check_button.click()
        time.sleep(0.5)
        assert 'completed' in tasks[0].find_element(By.TAG_NAME, 'span').get_attribute('class'), "A tarefa não foi marcada como concluída."

        # Editar a tarefa
        edit_button = tasks[0].find_element(By.CLASS_NAME, 'edit-btn')
        edit_button.click()
        time.sleep(0.5)

        # Aguardar até que o campo de entrada esteja presente e seja clicável
        edit_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//li[1]/input[@type="text"]'))
        )
        assert edit_input.get_attribute('value') == 'Teste tarefa 1', "O texto da tarefa para editar não está correto."
        edit_input.send_keys('Teste tarefa editada')
        edit_input.send_keys(Keys.ENTER)
        time.sleep(0.5)

# Aguardar até que a lista de tarefas seja atualizada
        WebDriverWait(driver, 5).until(
        EC.staleness_of(tasks[0])
        )

        # Verificar se a tarefa foi editada
        tasks = task_list.find_elements(By.TAG_NAME, 'li')
        assert tasks[0].find_element(By.TAG_NAME, 'span').text == 'Teste tarefa editada', "A tarefa não foi editada corretamente."

    # Excluir a tarefa
        # Excluir a tarefa
        task_to_delete = tasks[0]
        delete_button = task_to_delete.find_element(By.CLASS_NAME, 'delete-btn')
        delete_button.click()
        time.sleep(0.5)

    # Aguardar até que a tarefa seja excluída
        WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, f"//li[{tasks.index(task_to_delete) + 1}]"))
        )

    # Verificar se a tarefa foi excluída
        tasks = task_list.find_elements(By.TAG_NAME, 'li')
        assert len(tasks) == 0, "A tarefa não foi excluída corretamente."
        
        
        print("Todos os testes passaram.")
    finally:
        # Fechar o navegador
        driver.quit()

# Executar o teste
test_todo_list()
