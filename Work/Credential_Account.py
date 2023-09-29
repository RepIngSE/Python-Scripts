    '''
    Este código servirá para entrar a la cuenta de correo personal
    '''

    # Define las credenciales del correo electrónico que se utilizarán para iniciar sesión en Gmail.
    user = 'sara.cruz02@intouchcx.com'
    password = 'Saragabriela2604**'
    
    # Define la URL de Gmail que se abrirá en el navegador.
    urlSF= 'https://gmail.com'
    driver.get(urlSF)
    driver.maximize_window()
    
    # Define el tipo de localizador que se utilizará más adelante en el código.
    x = 'By.XPATH'
        
    # Espera hasta que el campo de entrada de correo electrónico sea visible y luego lo completa con el usuario.
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    element.send_keys(user)
    time.sleep(5)
    
    # Busca el botón "Next" y le hace clic.
    finder(selector, x, wait, driver)
    hijo = driver.find_element(By.XPATH, selector)
    padre = hijo.find_element(By.XPATH,'.//ancestor::button')
    padre.click()
    
    time.sleep(3)
    
    # Espera hasta que el campo de entrada de contraseña sea visible y luego lo completa con la contraseña.
    finder(selector, x, wait, driver)
    passwd = driver.find_element(By.XPATH, '//input[@name="Passwd"]').send_keys(password)
    time.sleep(5)
    
    # Busca nuevamente el botón "Next" y le hace clic.
    finder(selector, x, wait, driver)
    hijo = driver.find_element(By.XPATH, selector)
    padre = hijo.find_element(By.XPATH,'.//ancestor::button')
    padre.click()
    
    time.sleep(20)
