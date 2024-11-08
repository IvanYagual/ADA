import random

def generar_fichero_entrada_progresivo(nombre_fichero, num_casos, rango_presupuesto, rango_prendas, rango_modelos, rango_precios, incremento_modelos_por_caso):
    """
    Genera un archivo de pruebas en el que el número total de modelos aumenta progresivamente en cada caso.
    
    Args:
    - nombre_fichero (str): nombre del archivo de salida.
    - num_casos (int): número de casos a generar.
    - rango_presupuesto (tuple): rango (min, max) para el presupuesto de cada caso.
    - rango_prendas (tuple): rango (min, max) para el número de prendas en cada caso.
    - rango_modelos (tuple): rango (min, max) para el número inicial de modelos por prenda.
    - rango_precios (tuple): rango (min, max) para el precio de cada modelo.
    - incremento_modelos_por_caso (int): incremento en el número total de modelos en cada nuevo caso.
    """
    
    with open(nombre_fichero, 'w') as f:
        # Escribimos la cantidad total de casos en la primera línea
        f.write(f"{num_casos}\n")
        
        # Número total de modelos que deseamos en el primer caso
        num_modelos_total = 0
        
        for caso in range(num_casos):
            # Genera presupuesto aleatorio para el caso actual
            presupuesto = random.randint(*rango_presupuesto)
            # Genera un número de prendas aleatorio dentro del rango especificado
            num_prendas = random.randint(*rango_prendas)
            
            # Calcula el número total de modelos para este caso, aumentando progresivamente
            num_modelos_total += incremento_modelos_por_caso
            
            # Escribe la primera línea del caso con el presupuesto y el número de prendas
            f.write(f"{presupuesto} {num_prendas}\n")
            
            # Distribuimos los modelos en cada prenda para alcanzar el número total de modelos deseado
            modelos_restantes = num_modelos_total
            for prenda in range(num_prendas):
                # Asegúrate de que el número de modelos restantes no es menor que el número de prendas restantes
                modelos_minimos_por_prenda = max(1, modelos_restantes - (num_prendas - prenda - 1))
                num_modelos = random.randint(1, modelos_minimos_por_prenda) if prenda < num_prendas - 1 else modelos_restantes
                
                # Evita modelos negativos asegurando que `num_modelos` es al menos 1
                num_modelos = max(1, num_modelos)
                modelos_restantes -= num_modelos
                
                # Genera precios aleatorios para cada modelo con un rango mayor
                precios = [random.randint(*rango_precios) for _ in range(num_modelos)]
                
                # Escribe la línea con el número de modelos y sus precios
                f.write(f"{num_modelos} " + " ".join(map(str, precios)) + "\n")

# Ejemplo de uso con parámetros más grandes
generar_fichero_entrada_progresivo(
    nombre_fichero="casos_grandes2.in",
    num_casos=1000,  # Aumentamos el número de casos
    rango_presupuesto=(5000, 15000),  # Aumento del presupuesto
    rango_prendas=(5, 50),  # Aumento del número de prendas
    rango_modelos=(1000, 10000),  # Rango de modelos más grande
    rango_precios=(1, 50),  # Rango de precios mayor
    incremento_modelos_por_caso=500  # Incremento mayor de modelos por caso
)


