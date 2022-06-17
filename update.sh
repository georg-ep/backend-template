gcloud builds submit --tag gcr.io/dropship-350409/dropship-350409 /Users/georgepatterson/Desktop/Shopify-/ShopifyTemplateBE --project dropship-350409 && gcloud run deploy shopifytemplatebe \
--platform managed \
--region europe-west1 \
--project dropship-350409 \
--image gcr.io/dropship-350409/dropship-350409 \
--add-cloudsql-instances dropship-350409:europe-west1:sql \
--allow-unauthenticated \
--port 80

# List images: gcloud container images list --project dropship-350409

gcloud sql connect sql --user=shopifybe --database=postgres

# Create a user
CREATE USER admin WITH PASSWORD 'George123!' 
GRANT ALL PRIVILEGES ON DATABASE postgres to admin;