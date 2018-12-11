(ns campusfeed.env
  (:require [selmer.parser :as parser]
            [clojure.tools.logging :as log]
            [campusfeed.dev-middleware :refer [wrap-dev]]))

(def defaults
  {:init
   (fn []
     (parser/cache-off!)
     (log/info "\n-=[campusfeed started successfully using the development profile]=-"))
   :stop
   (fn []
     (log/info "\n-=[campusfeed has shut down successfully]=-"))
   :middleware wrap-dev})
