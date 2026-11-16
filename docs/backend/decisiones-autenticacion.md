
# Decisión arquitectónica: Autenticación y autorización

## 1. Autenticación

El sistema Tura Limpia implementa autenticación propia mediante correo electrónico o nombre de usuario y contraseña.

Las contraseñas se almacenan utilizando bcrypt.

Después de validar las credenciales, el sistema genera un token JWT firmado mediante HS256.

## 2. Autorización

La autorización se realiza mediante roles asociados a perfiles de usuario.

Roles definidos:
- ciudadano
- trabajador
- gerente
- admin

La dependencia `requiere_rol()` restringe el acceso a los endpoints según los roles autorizados.

## 3. OAuth 2.0 / OpenID Connect

Para la versión actual se adopta autenticación propia mediante JWT Bearer.

No se implementa un proveedor OAuth 2.0 u OpenID Connect externo en esta versión.

La arquitectura permite considerar su incorporación en futuras versiones si se requiere integración con proveedores de identidad externos.

## 4. Validaciones realizadas

- Login exitoso: HTTP 200.
- Consulta del usuario autenticado: HTTP 200.
- Acceso sin token: HTTP 401.
- Acceso con rol autorizado: HTTP 200.
- Acceso con rol no autorizado: HTTP 403.

## 5. Documentación

La API publica su documentación mediante:
- Swagger UI: /docs
- ReDoc: /redoc
- OpenAPI JSON: /openapi.json
