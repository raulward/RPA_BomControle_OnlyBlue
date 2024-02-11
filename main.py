from gui import State, RepeatOperationPage
from operation import operation, choose_download_directory, perform_login



def main():               
    state = State()

    login_page = perform_login(state)

    download_folder = choose_download_directory()

    if not download_folder or not login_page.is_closed_correctly():
        return

    operation(state, download_folder)


    repeat_operation = True

    while repeat_operation:
        repeat_operation_page = RepeatOperationPage()
        
        repeat_operation_page.wait_window()

        if repeat_operation_page.is_closed:
            repeat_operation = repeat_operation_page.repeat_operation

        if repeat_operation:
            operation(state, download_folder)
        if not repeat_operation_page.repeat_operation:
            break
        

if __name__ == "__main__":
    main()


