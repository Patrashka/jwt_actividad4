#!/usr/bin/env python3
"""
Alternativa a Redis usando diccionarios en memoria
Para desarrollo y pruebas cuando Redis no está disponible
"""

import json
import time
from datetime import datetime, timedelta
from threading import Lock
import logging

logger = logging.getLogger(__name__)

class InMemoryRedis:
    """Simulador de Redis usando diccionarios en memoria"""
    
    def __init__(self):
        self.data = {}
        self.expiry = {}
        self.lock = Lock()
        logger.info("Iniciando simulador Redis en memoria")
    
    def setex(self, key, ttl, value):
        """Establecer clave con TTL"""
        with self.lock:
            self.data[key] = value
            if ttl > 0:
                self.expiry[key] = time.time() + ttl
            else:
                self.expiry.pop(key, None)
            return True
    
    def get(self, key):
        """Obtener valor de clave"""
        with self.lock:
            # Verificar si la clave ha expirado
            if key in self.expiry and time.time() > self.expiry[key]:
                self.data.pop(key, None)
                self.expiry.pop(key, None)
                return None
            
            return self.data.get(key)
    
    def delete(self, key):
        """Eliminar clave"""
        with self.lock:
            self.data.pop(key, None)
            self.expiry.pop(key, None)
            return True
    
    def keys(self, pattern="*"):
        """Obtener claves que coincidan con el patrón"""
        with self.lock:
            # Limpiar claves expiradas primero
            current_time = time.time()
            expired_keys = [k for k, exp_time in self.expiry.items() if current_time > exp_time]
            for key in expired_keys:
                self.data.pop(key, None)
                self.expiry.pop(key, None)
            
            if pattern == "*":
                return list(self.data.keys())
            
            # Filtro simple para patrones
            import fnmatch
            return [k for k in self.data.keys() if fnmatch.fnmatch(k, pattern)]
    
    def lpush(self, key, *values):
        """Agregar valores al inicio de una lista"""
        with self.lock:
            if key not in self.data:
                self.data[key] = []
            elif not isinstance(self.data[key], list):
                self.data[key] = []
            
            for value in values:
                self.data[key].insert(0, value)
            return len(self.data[key])
    
    def lrange(self, key, start, end):
        """Obtener rango de elementos de una lista"""
        with self.lock:
            if key not in self.data or not isinstance(self.data[key], list):
                return []
            
            lst = self.data[key]
            if end == -1:
                end = len(lst) - 1
            
            return lst[start:end+1]
    
    def expire(self, key, ttl):
        """Establecer TTL para una clave existente"""
        with self.lock:
            if key in self.data:
                if ttl > 0:
                    self.expiry[key] = time.time() + ttl
                else:
                    self.expiry.pop(key, None)
                return True
            return False
    
    def ping(self):
        """Simular comando ping"""
        return "PONG"
    
    def close(self):
        """Cerrar conexión (no hace nada en memoria)"""
        pass
    
    def is_connected(self):
        """Verificar si está conectado (siempre True en memoria)"""
        return True

# Instancia global del simulador
in_memory_redis = InMemoryRedis()

def get_redis_client():
    """Obtener cliente Redis (real o simulado)"""
    try:
        import redis
        # Intentar conectar a Redis real
        client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        client.ping()  # Probar conexión
        logger.info("Conectado a Redis real")
        return client
    except:
        logger.warning("Redis no disponible, usando simulador en memoria")
        return in_memory_redis

if __name__ == "__main__":
    # Prueba del simulador
    redis_client = get_redis_client()
    
    print("Probando simulador Redis...")
    
    # Prueba básica
    redis_client.setex("test:key", 60, "test_value")
    value = redis_client.get("test:key")
    print(f"Set/Get: {value}")
    
    # Prueba de TTL
    redis_client.setex("test:ttl", 1, "expires_soon")
    time.sleep(2)
    expired_value = redis_client.get("test:ttl")
    print(f"TTL: {expired_value} (deberia ser None)")
    
    # Prueba de listas
    redis_client.lpush("test:list", "item1", "item2", "item3")
    items = redis_client.lrange("test:list", 0, -1)
    print(f"Lista: {items}")
    
    print("Simulador Redis funcionando correctamente!")

