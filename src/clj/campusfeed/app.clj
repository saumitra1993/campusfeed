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
    (GET "/get-posts-by-channel" [channel-id] (get-posts-by-channel channel-id))
    (GET "/posts/:post-id" [post-id] (get-post post-id))
    (GET "/get-channel-admins" [channel-id] (get-channel-admins channel-id))
    (GET "/channel/:channel-id" [channel-id] (get-channel channel-id))
    (GET "/get-channels-for-admin" [admin-id] (get-channels-for-admin admin-id))
  ))
