(ns user
  (:require [campusfeed.config :refer [env]]
            [clojure.spec.alpha :as s]
            [expound.alpha :as expound]
            [mount.core :as mount]
            [campusfeed.core :refer [start-app]]))

(alter-var-root #'s/*explain-out* (constantly expound/printer))

(defn start []
  (mount/start-without #'campusfeed.core/repl-server))

(defn stop []
  (mount/stop-except #'campusfeed.core/repl-server))

(defn restart []
  (stop)
  (start))


