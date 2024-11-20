import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random

class Usuario:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        # Patrones de uso (generados aleatoriamente para la simulación)
        self.patron_uso = {
            'consumo_datos': random.uniform(0, 100),  # MB por hora
            'tiempo_conexion': random.uniform(0, 24),  # Horas
            'actividad_principal': random.choice(['navegacion', 'streaming', 'gaming', 'trabajo'])
        }
        self.ancho_banda_asignado = 0

class RedWiFi:
    def __init__(self, n_usuarios, radio_cobertura):
        self.router_pos = (0, 0)  # Router en el centro
        self.radio_cobertura = radio_cobertura
        self.usuarios = self.generar_usuarios(n_usuarios)
        self.ancho_banda_total = 100  # MB por segundo
        
    def generar_usuarios(self, n):
        usuarios = []
        for i in range(n):
            # Generar posiciones aleatorias en coordenadas polares
            r = random.uniform(0, self.radio_cobertura)
            theta = random.uniform(0, 2 * np.pi)
            # Convertir a coordenadas cartesianas
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            usuarios.append(Usuario(x, y, i))
        return usuarios
    
    def clasificar_usuarios(self, n_clusters=3):
        # Preparar datos para clustering
        X = [[u.patron_uso['consumo_datos'], u.patron_uso['tiempo_conexion']] 
             for u in self.usuarios]
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Asignar ancho de banda basado en el cluster
        for usuario, cluster in zip(self.usuarios, clusters):
            if cluster == 0:  # Usuario de bajo consumo
                usuario.ancho_banda_asignado = self.ancho_banda_total * 0.1
            elif cluster == 1:  # Usuario medio
                usuario.ancho_banda_asignado = self.ancho_banda_total * 0.2
            else:  # Usuario de alto consumo
                usuario.ancho_banda_asignado = self.ancho_banda_total * 0.4
    
    def visualizar_red(self):
        # Crear figura y ejes
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Dibujar círculo de cobertura
        circle = plt.Circle(self.router_pos, self.radio_cobertura, 
                          fill=False, linestyle='--', color='gray')
        ax.add_patch(circle)
        
        # Dibujar router
        ax.plot(self.router_pos[0], self.router_pos[1], 'ks', 
                markersize=15, label='Router')
        
        # Crear scatter plot para los usuarios
        anchos_banda = [usuario.ancho_banda_asignado for usuario in self.usuarios]
        scatter = ax.scatter([usuario.x for usuario in self.usuarios],
                           [usuario.y for usuario in self.usuarios],
                           c=anchos_banda,
                           cmap='viridis')
        
        # Añadir etiquetas para cada usuario
        for usuario in self.usuarios:
            ax.annotate(f'ID: {usuario.id}\n{usuario.patron_uso["actividad_principal"]}',
                       (usuario.x, usuario.y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8)
        
        # Añadir barra de colores
        plt.colorbar(scatter, label='Ancho de banda asignado (MB/s)')
        
        plt.title('Simulación de Red Wi-Fi')
        plt.xlabel('Posición X')
        plt.ylabel('Posición Y')
        ax.set_aspect('equal')
        ax.grid(True)
        plt.show()

# Ejemplo de uso
def simular_red():
    # Crear una red con 15 usuarios y radio de cobertura de 10 unidades
    red = RedWiFi(n_usuarios=15, radio_cobertura=10)
    
    # Clasificar usuarios y asignar ancho de banda
    red.clasificar_usuarios()
    
    # Visualizar la red
    red.visualizar_red()
    
    # Imprimir información de los usuarios
    for usuario in red.usuarios:
        print(f"\nUsuario {usuario.id}:")
        print(f"Posición: ({usuario.x:.2f}, {usuario.y:.2f})")
        print(f"Actividad: {usuario.patron_uso['actividad_principal']}")
        print(f"Consumo de datos: {usuario.patron_uso['consumo_datos']:.2f} MB/h")
        print(f"Tiempo de conexión: {usuario.patron_uso['tiempo_conexion']:.2f} h")
        print(f"Ancho de banda asignado: {usuario.ancho_banda_asignado:.2f} MB/s")

if __name__ == "__main__":
    simular_red()
