(ns campusfeed.handler
  (:require [campusfeed.middleware :as middleware]
            [campusfeed.layout :refer [error-page]]
            [campusfeed.routes.home :refer [home-routes]]
            [compojure.core :refer [routes wrap-routes]]
            [ring.util.http-response :as response]
            [compojure.route :as route]
            [campusfeed.env :refer [defaults]]
            [mount.core :as mount]))

(mount/defstate init-app
  :start ((or (:init defaults) identity))
  :stop  ((or (:stop defaults) identity)))

(mount/defstate app
  :start
  (middleware/wrap-base
    (routes
      (-> #'home-routes
          (wrap-routes middleware/wrap-csrf)
          (wrap-routes middleware/wrap-formats))
      (route/not-found
        (:body
          (error-page {:status 404
                       :title "page not found"}))))))

