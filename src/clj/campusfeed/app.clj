(ns campusfeed.app
  (:require
    [compojure.core :refer [defroutes context GET POST]]
    [ring.util.http-response :refer [ok]]
    [campusfeed.api :as api]
    ))

(require 'campusfeed.src.clj.campusfeed.api)

(refer 'campusfeed.src.clj.campusfeed.api)

(defroutes api-routes
  (context "/api" []
    (GET "/hello/:name" [name] (ok {:message (api/greet name)}))
    (GET "/get-user-details" [userid] (get-user-details userid))
  ))
