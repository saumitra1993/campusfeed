(ns campusfeed.env
  (:require [clojure.tools.logging :as log]))

(def defaults
  {:init
   (fn []
     (log/info "\n-=[campusfeed started successfully]=-"))
   :stop
   (fn []
     (log/info "\n-=[campusfeed has shut down successfully]=-"))
   :middleware identity})
