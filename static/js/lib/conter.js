//  CONTER - BOX JS
(function ($) {
	"use strict"; 
    $.fn.appear = function (fn, options) {
        var settings = $.extend({
            data: undefined,
            one: true,
            accX: 0,
            accY: 0
        }, options);
        return this.each(function () {
            var t = $(this);
            t.appeared = false;
            if (!fn) {
                t.trigger('appear', settings.data);
                return;
            }
            var w = $(window);
            var check = function () {
                if (!t.is(':visible')) {
                    t.appeared = false;
                    return;
                }
                var a = w.scrollLeft();
                var b = w.scrollTop();
                var o = t.offset();
                var x = o.left;
                var y = o.top;
                var ax = settings.accX;
                var ay = settings.accY;
                var th = t.height();
                var wh = w.height();
                var tw = t.width();
                var ww = w.width();
                if (y + th + ay >= b && y <= b + wh + ay && x + tw + ax >= a && x <= a + ww + ax) {
                    if (!t.appeared) t.trigger('appear', settings.data);
                } else {
                    t.appeared = false;
                }
            };
            var modifiedFn = function () {
                t.appeared = true;
                if (settings.one) {
                    w.unbind('scroll', check);
                    var i = $.inArray(check, $.fn.appear.checks);
                    if (i >= 0) $.fn.appear.checks.splice(i, 1);
                }
                fn.apply(this, arguments);
            };
            if (settings.one) t.one('appear', settings.data, modifiedFn);
            else t.bind('appear', settings.data, modifiedFn);
            w.scroll(check);
            $.fn.appear.checks.push(check);
            (check)();
        });
    };
    $.extend($.fn.appear, {
        checks: [],
        timeout: null,
        checkAll: function () {
            var length = $.fn.appear.checks.length;
        },
        run: function () {
            if ($.fn.appear.timeout) clearTimeout($.fn.appear.timeout);
            $.fn.appear.timeout = setTimeout($.fn.appear.checkAll, 20);
        }
    });
    $.each(['append', 'prepend', 'after', 'before', 'attr', 'removeAttr', 'addClass', 'removeClass', 'toggleClass', 'remove', 'css', 'show', 'hide'], function (i, n) {
        var old = $.fn[n];
        if (old) {
            $.fn[n] = function () {
                var r = old.apply(this, arguments);
                $.fn.appear.run();
                return r;
            }
        }
    });
})(jQuery);
// Count Value
(function ($) {
    var Reg_Email = /^\w+([\-\.]\w+)*@([a-z0-9]+(\-+[a-z0-9]+)?\.)+[a-z]{2,5}$/i,
        $window = $(window),
        $windowHeight = $(window)
        .height(),
        $documentHeight = $(document)
        .height(),
        $windowWidth = $(window)
        .width(),
        $wpAdminBarHeight = $('#wpadminbar')
        .height(),
        num, mainHeight = $('body')
        .height(),
        $checkFixed = $("#pxHeader")
        .attr("data-fixed"),
        scroll, scrollto, pageRefresh = true,
        content = false,
        ajaxLoading = false,
        projectContainer = $('#portfolioDetailAjax'),
        portfolioGrid = $('#isotopePortfolio'),
        wrapperHeight, folderName = 'portfolio-detail',
        loader = $('.portfolioSection #loader'),
        pDError = $('#pDError'),
        pDetailNav = $('.navCloseWrap'),
        hash = $(window.location)
        .attr('hash'),
        root = '#!' + folderName + '/',
        rootLength = root.length,
        videoWidthOriginal = 1280,
        videoHeightOriginal = 720,
        minW = 1500,
        vidRatio = 1280 / 720,
        scrollpals = $("html, body"),
        isTouchDevice = 'ontouchstart' in window || 'onmsgesturechange' in window;

    function piechart() {
        "use strict";
        if ($(window)
            .width() > 1024) {
            var $pieChartBox = $('.pieChartBox')
                .not('.pieChartWithAnimation');
        } else {
            var $pieChartBox = $('.pieChartBox');
        } if (!$pieChartBox.length) return;
        $pieChartBox.each(function () {
            $(this)
                .find('.easyPieChart')
                .easyPieChart({
                    scaleColor: false,
                    barColor: $(this)
                        .attr('data-barColor'),
                    lineWidth: 12,
                    trackColor: 'rgba(233,230,230,0.3)',
                    lineCap: 'butt',
                    easing: 'easeInQuart',
                    animate: {
                        duration: 3000,
                        enabled: true
                    },
                    size: 145
                });
        });
    }

    function piechartAnimate() {
        "use strict";
        var $pieChartBox = $('.pieChartWithAnimation');
        if (!$pieChartBox.length) return;
        $pieChartBox.each(function () {
            $(this)
                .find('.easyPieChart')
                .easyPieChart({
                    scaleColor: false,
                    barColor: $(this)
                        .attr('data-barColor'),
                    lineWidth: 12,
                    trackColor: 'rgba(233,230,230,0.3)',
                    lineCap: 'butt',
                    easing: 'easeInQuart',
                    animate: {
                        duration: 3000,
                        enabled: true
                    },
                    size: 145
                });
        });
    }

    function counterBox() {
        "use strict";
        if ($(window)
            .width() > 1024) {
            var $counterBoxContainers = $('.counterBox')
                .not('.counterWithAnimation');
        } else {
            var $counterBoxContainers = $('.counterBox');
        } if (!$counterBoxContainers.length) return;
        $counterBoxContainers.each(function () {
            var countNmber = $(this)
                .attr('data-countNmber');
            $(this)
                .find('.counterBoxNumber')
                .countTo({
                    from: 0,
                    to: countNmber,
                    speed: 1250,
                    refreshInterval: 100
                });
        });
    }

    function counterBoxAnimate() {
        "use strict";
        var $counterBoxContainers = $('.counterWithAnimation');
        if (!$counterBoxContainers.length) return;
        $counterBoxContainers.each(function () {
            var countNmber = $(this)
                .attr('data-countNmber');
            $(this)
                .find('.counterBoxNumber')
                .countTo({
                    from: 0,
                    to: countNmber,
                    speed: 1250,
                    refreshInterval: 100
                });
        });
    }

    function shortcodeAnimation() {
        "use strict";
        if ($(window)
            .width() > 1024) {
            $('.imgWithAnimation')
                .add('.textWithAnimation')
                .add('.iconWithAnimation')
                .add('.teamWithAnimation')
                .add('.counterWithAnimation')
                .add('.pieChartWithAnimation')
                .each(function () {
                    var $daly = $(this)
                        .attr('data-delay');
                    $(this)
                        .appear(function () {
                            if ($(this)
                                .attr('data-animation') == 'fade-in-left') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            avoidTransforms: true,
                                            useTranslate3d: true,
                                            'opacity': 1,
                                            'left': '-80px',
                                            'right': '0px'
                                        }, {
                                            complete: function () {
                                                $(this)
                                                    .css({
                                                        'right': '0px',
                                                        'left': '0px'
                                                    });
                                                $(this)
                                                    .addClass('notransitionleft');
                                            },
                                            easing: 'easeOutSine',
                                            duration: 800
                                        });
                                }), $daly);
                                if ($(item)
                                    .hasClass("counterBox")) {
                                    counterBoxAnimate();
                                }
                                if ($(item)
                                    .hasClass("pieChartBox")) {
                                    piechartAnimate();
                                }
                            } else if ($(this)
                                .attr('data-animation') == 'fade-in-right') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            'opacity': 1,
                                            'right': '-80px'
                                        }, {
                                            complete: function () {
                                                $(this)
                                                    .css({
                                                        'left': '0px'
                                                    });
                                            },
                                            easing: 'easeOutSine',
                                            duration: 800
                                        });
                                }), $daly);
                                if ($(item)
                                    .hasClass("counterBox")) {
                                    counterBoxAnimate();
                                }
                                if ($(item)
                                    .hasClass("pieChartBox")) {
                                    piechartAnimate();
                                }
                            } else if ($(this)
                                .attr('data-animation') == 'fade-in-bottom') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            'opacity': 1,
                                            'left': '0px'
                                        }, 800, 'easeOutSine');
                                    $(item)
                                        .animate({
                                            'opacity': 1,
                                            'bottom': '-70px'
                                        }, {
                                            complete: function () {
                                                $(this)
                                                    .css({
                                                        'top': '0px'
                                                    });
                                                $(this)
                                                    .addClass('notransition');
                                            },
                                            easing: 'easeOutSine',
                                            duration: 800
                                        });
                                }), $daly);
                                if ($(this)
                                    .hasClass("counterBox")) {
                                    counterBoxAnimate();
                                }
                                if ($(this)
                                    .hasClass("pieChartBox")) {
                                    piechartAnimate();
                                }
                            } else if ($(this)
                                .attr('data-animation') == 'fade-in-top') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            'opacity': 1,
                                            'top': '0px'
                                        }, 800, 'easeOutSine');
                                    if ($(item)
                                        .hasClass("counterBox")) {
                                        counterBoxAnimate();
                                    }
                                    if ($(item)
                                        .hasClass("pieChartBox")) {
                                        piechartAnimate();
                                    }
                                }), $daly);
                            } else if ($(this)
                                .attr('data-animation') == 'fade-in') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            'opacity': 1
                                        }, 800, 'easeOutSine');
                                }), $daly);
                                if ($(item)
                                    .hasClass("counterBox")) {
                                    counterBoxAnimate();
                                }
                                if ($(item)
                                    .hasClass("pieChartBox")) {
                                    piechartAnimate();
                                }
                            } else if ($(this)
                                .attr('data-animation') == 'grow-in') {
                                var $that = $(this);
                                setTimeout(function () {
                                    $that.transition({
                                        scale: 1,
                                        'opacity': 1
                                    }, 900, 'cubic-bezier(0.15, 0.84, 0.35, 1.25)');
                                }, $daly);
                                if ($(this)
                                    .hasClass("counterBox")) {
                                    counterBoxAnimate();
                                }
                                if ($(this)
                                    .hasClass("pieChartBox")) {}
                            }
                        }, {
                            accX: 0,
                            accY: -100
                        }, 'easeInCubic');
                    $(this)
                        .appear(function () {
                            if ($(this)
                                .attr('data-animation') == 'fade-in-top') {
                                var item = this;
                                setTimeout((function () {
                                    $(item)
                                        .animate({
                                            'opacity': 1,
                                            'top': '0px'
                                        }, 800, 'easeOutSine');
                                    if ($(item)
                                        .hasClass("counterBox")) {
                                        counterBoxAnimate();
                                    }
                                    if ($(item)
                                        .hasClass("pieChartBox")) {
                                        piechartAnimate();
                                    }
                                }), $daly);
                            }
                        }, {
                            accX: 0,
                            accY: 100
                        }, 'easeInCubic');
                });
        }
    }
    $(function () {
        (function (k) {
            k.transit = {
                version: "0.9.9",
                propertyMap: {
                    marginLeft: "margin",
                    marginRight: "margin",
                    marginBottom: "margin",
                    marginTop: "margin",
                    paddingLeft: "padding",
                    paddingRight: "padding",
                    paddingBottom: "padding",
                    paddingTop: "padding"
                },
                enabled: true,
                useTransitionEnd: false
            };
            var d = document.createElement("div");
            var q = {};

            function b(v) {
                if (v in d.style) {
                    return v
                }
                var u = ["Moz", "Webkit", "O", "ms"];
                var r = v.charAt(0)
                    .toUpperCase() + v.substr(1);
                if (v in d.style) {
                    return v
                }
                for (var t = 0; t < u.length; ++t) {
                    var s = u[t] + r;
                    if (s in d.style) {
                        return s
                    }
                }
            }

            function e() {
                d.style[q.transform] = "";
                d.style[q.transform] = "rotateY(90deg)";
                return d.style[q.transform] !== ""
            }
            var a = navigator.userAgent.toLowerCase()
                .indexOf("chrome") > -1;
            q.transition = b("transition");
            q.transitionDelay = b("transitionDelay");
            q.transform = b("transform");
            q.transformOrigin = b("transformOrigin");
            q.transform3d = e();
            var i = {
                transition: "transitionEnd",
                MozTransition: "transitionend",
                OTransition: "oTransitionEnd",
                WebkitTransition: "webkitTransitionEnd",
                msTransition: "MSTransitionEnd"
            };
            var f = q.transitionEnd = i[q.transition] || null;
            for (var p in q) {
                if (q.hasOwnProperty(p) && typeof k.support[p] === "undefined") {
                    k.support[p] = q[p]
                }
            }
            d = null;
            k.cssEase = {
                _default: "ease",
                "in": "ease-in",
                out: "ease-out",
                "in-out": "ease-in-out",
                snap: "cubic-bezier(0,1,.5,1)",
                easeOutCubic: "cubic-bezier(.215,.61,.355,1)",
                easeInOutCubic: "cubic-bezier(.645,.045,.355,1)",
                easeInCirc: "cubic-bezier(.6,.04,.98,.335)",
                easeOutCirc: "cubic-bezier(.075,.82,.165,1)",
                easeInOutCirc: "cubic-bezier(.785,.135,.15,.86)",
                easeInExpo: "cubic-bezier(.95,.05,.795,.035)",
                easeOutExpo: "cubic-bezier(.19,1,.22,1)",
                easeInOutExpo: "cubic-bezier(1,0,0,1)",
                easeInQuad: "cubic-bezier(.55,.085,.68,.53)",
                easeOutQuad: "cubic-bezier(.25,.46,.45,.94)",
                easeInOutQuad: "cubic-bezier(.455,.03,.515,.955)",
                easeInQuart: "cubic-bezier(.895,.03,.685,.22)",
                easeOutQuart: "cubic-bezier(.165,.84,.44,1)",
                easeInOutQuart: "cubic-bezier(.77,0,.175,1)",
                easeInQuint: "cubic-bezier(.755,.05,.855,.06)",
                easeOutQuint: "cubic-bezier(.23,1,.32,1)",
                easeInOutQuint: "cubic-bezier(.86,0,.07,1)",
                easeInSine: "cubic-bezier(.47,0,.745,.715)",
                easeOutSine: "cubic-bezier(.39,.575,.565,1)",
                easeInOutSine: "cubic-bezier(.445,.05,.55,.95)",
                easeInBack: "cubic-bezier(.6,-.28,.735,.045)",
                easeOutBack: "cubic-bezier(.175, .885,.32,1.275)",
                easeInOutBack: "cubic-bezier(.68,-.55,.265,1.55)"
            };
            k.cssHooks["transit:transform"] = {
                get: function (r) {
                    return k(r)
                        .data("transform") || new j()
                },
                set: function (s, r) {
                    var t = r;
                    if (!(t instanceof j)) {
                        t = new j(t)
                    }
                    if (q.transform === "WebkitTransform" && !a) {
                        s.style[q.transform] = t.toString(true)
                    } else {
                        s.style[q.transform] = t.toString()
                    }
                    k(s)
                        .data("transform", t)
                }
            };
            k.cssHooks.transform = {
                set: k.cssHooks["transit:transform"].set
            };
            if (k.fn.jquery < "1.8") {
                k.cssHooks.transformOrigin = {
                    get: function (r) {
                        return r.style[q.transformOrigin]
                    },
                    set: function (r, s) {
                        r.style[q.transformOrigin] = s
                    }
                };
                k.cssHooks.transition = {
                    get: function (r) {
                        return r.style[q.transition]
                    },
                    set: function (r, s) {
                        r.style[q.transition] = s
                    }
                }
            }
            n("scale");
            n("translate");
            n("rotate");
            n("rotateX");
            n("rotateY");
            n("rotate3d");
            n("perspective");
            n("skewX");
            n("skewY");
            n("x", true);
            n("y", true);

            function j(r) {
                if (typeof r === "string") {
                    this.parse(r)
                }
                return this
            }
            j.prototype = {
                setFromString: function (t, s) {
                    var r = (typeof s === "string") ? s.split(",") : (s.constructor === Array) ? s : [s];
                    r.unshift(t);
                    j.prototype.set.apply(this, r)
                },
                set: function (s) {
                    var r = Array.prototype.slice.apply(arguments, [1]);
                    if (this.setter[s]) {
                        this.setter[s].apply(this, r)
                    } else {
                        this[s] = r.join(",")
                    }
                },
                get: function (r) {
                    if (this.getter[r]) {
                        return this.getter[r].apply(this)
                    } else {
                        return this[r] || 0
                    }
                },
                setter: {
                    rotate: function (r) {
                        this.rotate = o(r, "deg")
                    },
                    rotateX: function (r) {
                        this.rotateX = o(r, "deg")
                    },
                    rotateY: function (r) {
                        this.rotateY = o(r, "deg")
                    },
                    scale: function (r, s) {
                        if (s === undefined) {
                            s = r
                        }
                        this.scale = r + "," + s
                    },
                    skewX: function (r) {
                        this.skewX = o(r, "deg")
                    },
                    skewY: function (r) {
                        this.skewY = o(r, "deg")
                    },
                    perspective: function (r) {
                        this.perspective = o(r, "px")
                    },
                    x: function (r) {
                        this.set("translate", r, null)
                    },
                    y: function (r) {
                        this.set("translate", null, r)
                    },
                    translate: function (r, s) {
                        if (this._translateX === undefined) {
                            this._translateX = 0
                        }
                        if (this._translateY === undefined) {
                            this._translateY = 0
                        }
                        if (r !== null && r !== undefined) {
                            this._translateX = o(r, "px")
                        }
                        if (s !== null && s !== undefined) {
                            this._translateY = o(s, "px")
                        }
                        this.translate = this._translateX + "," + this._translateY
                    }
                },
                getter: {
                    x: function () {
                        return this._translateX || 0
                    },
                    y: function () {
                        return this._translateY || 0
                    },
                    scale: function () {
                        var r = (this.scale || "1,1")
                            .split(",");
                        if (r[0]) {
                            r[0] = parseFloat(r[0])
                        }
                        if (r[1]) {
                            r[1] = parseFloat(r[1])
                        }
                        return (r[0] === r[1]) ? r[0] : r
                    },
                    rotate3d: function () {
                        var t = (this.rotate3d || "0,0,0,0deg")
                            .split(",");
                        for (var r = 0; r <= 3; ++r) {
                            if (t[r]) {
                                t[r] = parseFloat(t[r])
                            }
                        }
                        if (t[3]) {
                            t[3] = o(t[3], "deg")
                        }
                        return t
                    }
                },
                parse: function (s) {
                    var r = this;
                    s.replace(/([a-zA-Z0-9]+)\((.*?)\)/g, function (t, v, u) {
                        r.setFromString(v, u)
                    })
                },
                toString: function (t) {
                    var s = [];
                    for (var r in this) {
                        if (this.hasOwnProperty(r)) {
                            if ((!q.transform3d) && ((r === "rotateX") || (r === "rotateY") || (r === "perspective") || (r === "transformOrigin"))) {
                                continue
                            }
                            if (r[0] !== "_") {
                                if (t && (r === "scale")) {
                                    s.push(r + "3d(" + this[r] + ",1)")
                                } else {
                                    if (t && (r === "translate")) {
                                        s.push(r + "3d(" + this[r] + ",0)")
                                    } else {
                                        s.push(r + "(" + this[r] + ")")
                                    }
                                }
                            }
                        }
                    }
                    return s.join(" ")
                }
            };

            function m(s, r, t) {
                if (r === true) {
                    s.queue(t)
                } else {
                    if (r) {
                        s.queue(r, t)
                    } else {
                        t()
                    }
                }
            }

            function h(s) {
                var r = [];
                k.each(s, function (t) {
                    t = k.camelCase(t);
                    t = k.transit.propertyMap[t] || k.cssProps[t] || t;
                    t = c(t);
                    if (k.inArray(t, r) === -1) {
                        r.push(t)
                    }
                });
                return r
            }

            function g(s, v, x, r) {
                var t = h(s);
                if (k.cssEase[x]) {
                    x = k.cssEase[x]
                }
                var w = "" + l(v) + " " + x;
                if (parseInt(r, 10) > 0) {
                    w += " " + l(r)
                }
                var u = [];
                k.each(t, function (z, y) {
                    u.push(y + " " + w)
                });
                return u.join(", ")
            }
            k.fn.transition = k.fn.transit = function (z, s, y, C) {
                var D = this;
                var u = 0;
                var w = true;
                if (typeof s === "function") {
                    C = s;
                    s = undefined
                }
                if (typeof y === "function") {
                    C = y;
                    y = undefined
                }
                if (typeof z.easing !== "undefined") {
                    y = z.easing;
                    delete z.easing
                }
                if (typeof z.duration !== "undefined") {
                    s = z.duration;
                    delete z.duration
                }
                if (typeof z.complete !== "undefined") {
                    C = z.complete;
                    delete z.complete
                }
                if (typeof z.queue !== "undefined") {
                    w = z.queue;
                    delete z.queue
                }
                if (typeof z.delay !== "undefined") {
                    u = z.delay;
                    delete z.delay
                }
                if (typeof s === "undefined") {
                    s = k.fx.speeds._default
                }
                if (typeof y === "undefined") {
                    y = k.cssEase._default
                }
                s = l(s);
                var E = g(z, s, y, u);
                var B = k.transit.enabled && q.transition;
                var t = B ? (parseInt(s, 10) + parseInt(u, 10)) : 0;
                if (t === 0) {
                    var A = function (F) {
                        D.css(z);
                        if (C) {
                            C.apply(D)
                        }
                        if (F) {
                            F()
                        }
                    };
                    m(D, w, A);
                    return D
                }
                var x = {};
                var r = function (H) {
                    var G = false;
                    var F = function () {
                        if (G) {
                            D.unbind(f, F)
                        }
                        if (t > 0) {
                            D.each(function () {
                                this.style[q.transition] = (x[this] || null)
                            })
                        }
                        if (typeof C === "function") {
                            C.apply(D)
                        }
                        if (typeof H === "function") {
                            H()
                        }
                    };
                    if ((t > 0) && (f) && (k.transit.useTransitionEnd)) {
                        G = true;
                        D.bind(f, F)
                    } else {
                        window.setTimeout(F, t)
                    }
                    D.each(function () {
                        if (t > 0) {
                            this.style[q.transition] = E
                        }
                        k(this)
                            .css(z)
                    })
                };
                var v = function (F) {
                    this.offsetWidth;
                    r(F)
                };
                m(D, w, v);
                return this
            };

            function n(s, r) {
                if (!r) {
                    k.cssNumber[s] = true
                }
                k.transit.propertyMap[s] = q.transform;
                k.cssHooks[s] = {
                    get: function (v) {
                        var u = k(v)
                            .css("transit:transform");
                        return u.get(s)
                    },
                    set: function (v, w) {
                        var u = k(v)
                            .css("transit:transform");
                        u.setFromString(s, w);
                        k(v)
                            .css({
                                "transit:transform": u
                            })
                    }
                }
            }

            function c(r) {
                return r.replace(/([A-Z])/g, function (s) {
                    return "-" + s.toLowerCase()
                })
            }

            function o(s, r) {
                if ((typeof s === "string") && (!s.match(/^[\-0-9\.]+$/))) {
                    return s
                } else {
                    return "" + s + r
                }
            }

            function l(s) {
                var r = s;
                if (k.fx.speeds[r]) {
                    r = k.fx.speeds[r]
                }
                return o(r, "ms")
            }
            k.transit.getTransitionValue = g
        })(jQuery);
    });
    $(window)
        .load(function () {
            $('#startLoader')
                .fadeOut(850);
            shortcodeAnimation();
        });
    $(window)
        .scroll(function () {
            function headerTransform() {
                var $hideMeunScrollHeight = $windowHeight * 0.08;
                if ($window_y > $hideMeunScrollHeight && $checkFixed === 'scroll-sticky') {
                    $("#pxHeader")
                        .fadeIn(300);
                } else if ($window_y > $hideMeunScrollHeight && $checkFixed === 'scooter-menu') {
                    var $checkShowMenu = $('#pxHeader')
                        .hasClass('hideHeaderShadow');
                    if ($checkShowMenu) {
                        $('#logoMenuHeader')
                            .fadeIn('fast', function () {
                                $('#logoHeader')
                                    .fadeOut('fast');
                            });
                        $('#pxHeader')
                            .removeClass('hideHeaderShadow');
                    }
                } else {
                    if ($checkFixed === 'scroll-sticky') {
                        $("#pxHeader")
                            .fadeOut(300);
                    } else if ($checkFixed === 'scooter-menu') {
                        var $checkShowMenu = $('#pxHeader')
                            .hasClass('hideHeaderShadow');
                        if (!$checkShowMenu) {
                            $('#logoHeader')
                                .fadeIn('fast', function () {
                                    $('#logoMenuHeader')
                                        .fadeOut('slow');
                                });
                            $('#pxHeader')
                                .addClass('hideHeaderShadow');
                        }
                    }
                }
            }
        });
})(jQuery);
(function ($) {
    $.fn.countTo = function (options) {
        options = options || {};
        return $(this)
            .each(function () {
                var settings = $.extend({}, $.fn.countTo.defaults, {
                    from: $(this)
                        .data('from'),
                    to: $(this)
                        .data('to'),
                    speed: $(this)
                        .data('speed'),
                    refreshInterval: $(this)
                        .data('refresh-interval'),
                    decimals: $(this)
                        .data('decimals')
                }, options);
                var loops = Math.ceil(settings.speed / settings.refreshInterval),
                    increment = (settings.to - settings.from) / loops;
                var self = this,
                    $self = $(this),
                    loopCount = 0,
                    value = settings.from,
                    data = $self.data('countTo') || {};
                $self.data('countTo', data);
                if (data.interval) {
                    clearInterval(data.interval);
                }
                data.interval = setInterval(updateTimer, settings.refreshInterval);
                render(value);

                function updateTimer() {
                    value += increment;
                    loopCount++;
                    render(value);
                    if (typeof (settings.onUpdate) == 'function') {
                        settings.onUpdate.call(self, value);
                    }
                    if (loopCount >= loops) {
                        $self.removeData('countTo');
                        clearInterval(data.interval);
                        value = settings.to;
                        if (typeof (settings.onComplete) == 'function') {
                            settings.onComplete.call(self, value);
                        }
                    }
                }

                function render(value) {
                    var formattedValue = settings.formatter.call(self, value, settings);
                    $self.text(formattedValue);
                }
            });
    };
    $.fn.countTo.defaults = {
        from: 0,
        to: 0,
        speed: 1000,
        refreshInterval: 100,
        decimals: 0,
        formatter: formatter,
        onUpdate: null,
        onComplete: null
    };

    function formatter(value, settings) {
        return value.toFixed(settings.decimals);
    }
}(jQuery));
//  # COUNT & # CONTER - BOX