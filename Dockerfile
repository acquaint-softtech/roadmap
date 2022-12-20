FROM python:3.8.10

WORKDIR /Roadmap

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT 'developments'
ENV SECRET_KEY 'django-insecure-#gv1xsoa&_51f23egl0ik76@qint-dx%)s+it34j%#wp655m60'
# database configurations
ENV DB_ENGINE 'django.db.backends.postgresql_psycopg2'
ENV DB_NAME 'roadmap'
ENV DB_USER 'postgres'
ENV DB_PASSWORD 'postgres'
ENV DB_HOST 'db'
ENV DB_PORT '5432'

#OIDC configurations
ENV OIDC_RP_CLIENT_ID '41d637e0-4099-013b-4350-0287d41bf759218436'
ENV OIDC_RP_CLIENT_SECRET 'b4777d4406e1bb1c438931fe01993303a6a926946ebc79ed707edc33ae2be912'
ENV OIDC_OP_AUTHORIZATION_ENDPOINT 'https://roadmap.onelogin.com/oidc/2/auth'
ENV OIDC_OP_TOKEN_ENDPOINT 'https://roadmap.onelogin.com/oidc/2/token'
ENV OIDC_OP_USER_ENDPOINT 'https://roadmap.onelogin.com/oidc/2/me'
ENV OIDC_RP_SIGN_ALGO 'RS256'
ENV OIDC_OP_JWKS_ENDPOINT 'https://contentlab-dev.onelogin.com/oidc/2/certs'
ENV LOGIN_REDIRECT_URL 'http://localhost:8000/'
ENV LOGOUT_REDIRECT_URL 'http://localhost:8000/'

# ENV NPM_BIN_PATH "/usr/local/bin/npm"

# ENV TAILWIND_CSS_PATH 'css/dist/styles.css'

# ENV NPM_BIN_PATH "/usr/local/bin/npm"

# install dependencies
COPY requirements.txt /Roadmap/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install --upgrade Pillow

# ENV NODE_PATH '/user_themes/static_src/node_modules'

# copy project
COPY . .
