from playwright.sync_api import  sync_playwright

from time import sleep
import vars
import os


from gui import LoginPage, EmpresaPage, State, choose_download_directory, RepeatOperationPage

def operation(state, download_folder): 
     with sync_playwright() as p:
          try:
               # Iniciando o chrome
               browser = p.chromium.launch(headless=True)
               context = browser.new_context(accept_downloads=True, base_url=vars.URL_BOMCONTROLE)

               # Passando o contexto do browser para a pagina
               page = context.new_page()
               sleep(1)

               # Redirecionando para a pagina de login
               page.goto('login')
               sleep(1)

               # Localizando o elemento do campo de email e enviando dados
               input_email = page.wait_for_selector(vars.CSS_INPUT_EMAIL)
               
               if input_email:
                    input_email.fill(state.email)
               sleep(1)

               # Localizando o botao de enviar (email) e clickando
               page.wait_for_selector('button').click()
               sleep(3)

               # Localizando o elemento do campo senha e enviando dados
               page.wait_for_selector('input').fill(state.password)
               
               # Localizando o botao de enviar (senha) e clickando
               page.wait_for_selector('button').click()
               sleep(3)

               # Verificando a existencia do botao apos o login
               element = page.eval_on_selector('button', 'element => element !== null')
               sleep(2)

               # Caso o elemento exista, procura-lo e clicka-lo
               sleep(2)
               if element:
                    page.locator('button').nth(0).click()
                    sleep(2)
               else:
                    print('Elemento nao encontrado ou removido')

               # Indo para a pagina da dre
               page.goto('financeiro/informacoes-dre')
               sleep(2)
               
               # Selecionando o dropdown das empresas
               element_dropdown = page.locator(vars.CSS_EMPRESAS)
               element_dropdown.click()
               sleep(2)

               # Obtendo os elementos das empresas no dropdown
               empresas = page.locator(vars.CSS_LISTA_EMPRESAS).element_handles()

               empresa_page = EmpresaPage(state, empresas)
               empresa_page.show()

               choice = empresa_page.get_choice()
               empresa_page.confirm()

               if choice is not None:

                    # Clickando na empresa
                    empresas[choice].click()

                    # Localizando e clickando no botao de competencia
                    page.locator(vars.CSS_DROPDOWN_CAIXA).nth(1).click()
                              
                    # Localizando o item do dropdown pelo texto e clicando nele
                    page.locator('.ui-select-choices-row:nth-child(2)').click()

                    # Localizando e clickando no botao de competencia
                    page.locator(vars.CSS_DROPDOWN_CAIXA).nth(1).click()

                    # Localizando o botao da caixa
                    sleep(2)
                    # Localizando o item do dropdown pelo texto e clicando nele
                    page.locator('.ui-select-choices-row:nth-child(2)').click()

                    # Aguarde até que o botão de aplicar esteja disponível
                    page.wait_for_selector(vars.CSS_BTN_APLICAR).click()


                    # Aguarde até que o botão de exportar esteja disponível
                    page.wait_for_selector(vars.CSS_BTN_EXPORTAR).click()
                    sleep(2)

                    # Aguarde até que o botão de CSV esteja disponível
                    with page.expect_download() as download_info:
                         page.wait_for_selector(vars.CSS_BTN_XLS).click()

                    download = download_info.value
                    suggested_filename = download.suggested_filename
                         
                    counter = 1

                    output_filepath = os.path.join(download_folder, suggested_filename)
                         

                    while os.path.exists(output_filepath):
                         # Adicionar (1), (2), etc., ao nome do arquivo
                         base_filename, extension = os.path.splitext(suggested_filename)
                         suggested_filename = f"{base_filename}_{counter}{extension}"
                         output_filepath = os.path.join(download_folder, suggested_filename)
                         counter += 1

                    download.save_as(output_filepath)
                    sleep(2)

                         

          except Exception as e:
               print(f'Erro durante a execucao do bot: {e}')
          finally:
               browser.close()


def main():               
     
     state = State()
     login_page = LoginPage(state)
     login_page.load_state()
     login_page.mainloop()

     download_folder = choose_download_directory()
          
     if not download_folder:
          return


     if not login_page.is_closed_correctly():
          return
     
     repeat_operation = True
     
     while repeat_operation:
        
        operation(state, download_folder)

        repeat_page = RepeatOperationPage()
        repeat_page.repeat_fun(operation, state, download_folder)
        repeat_page.mainloop()

        repeat_operation = repeat_page.repeat_operation


if __name__ == "__main__":
     main()
