terraform {
  backend "gcs" {
    bucket = "tf-state-flask-kube-joc"   # schimbă dacă vrei alt nume
    prefix = "terraform/state"
  }
}
