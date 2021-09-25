var f = !1
          , m = function() {
            function e() {
                !function(e, t) {
                    if (!(e instanceof t))
                        throw new TypeError("Cannot call a class as a function")
                }(this, e),
                this.limit = 35,
                this.particles = [],
                this.autoAddParticle = !1,
                this.sizes = [15, 20, 25, 35, 45],
                this.variants = ["\ud83c\udf08"],
                this.addHandlers(),
                this.loop()
            }
            var t, n, a;
            return t = e,
            (n = [{
                key: "loop",
                value: function() {
                    this.autoAddParticle && this.particles.length < this.limit && this.createParticle(),
                    this.updateParticles(),
                    requestAnimationFrame(this.loop.bind(this))
                }
            }, {
                key: "addHandlers",
                value: function() {
                    var e = this
                      , t = "ontouchstart"in window || navigator.msMaxTouchPoints
                      , n = t ? "touchstart" : "mousedown"
                      , a = t ? "touchend" : "mouseup"
                      , i = t ? "touchmove" : "mousemove";
                    f || (f = !0,
                    document.addEventListener(i, (function(t) {
                        var n, a;
                        e.mouseX = t.pageX || (null === (n = t.touches) || void 0 === n ? void 0 : n[0].pageX),
                        e.mouseY = t.pageY || (null === (a = t.touches) || void 0 === a ? void 0 : a[0].pageY)
                    }
                    ), {
                        passive: !1
                    }),
                    document.addEventListener(n, (function(t) {
                        var n, a;
                        e.mouseX = t.pageX || (null === (n = t.touches[0]) || void 0 === n ? void 0 : n.pageX),
                        e.mouseY = t.pageY || (null === (a = t.touches[0]) || void 0 === a ? void 0 : a.pageY),
                        e.autoAddParticle = !0
                    }
                    )),
                    document.addEventListener(a, (function() {
                        e.autoAddParticle = !1
                    }
                    )),
                    document.addEventListener("mouseleave", (function() {
                        e.autoAddParticle = !1
                    }
                    )))
                }
            }, {


key: "createParticle",
value: function() {
    if ("/" === window.location.pathname) {
        var e = this.sizes[Math.floor(Math.random() * this.sizes.length)]
          , t = 10 * Math.random()
          , n = 25 * Math.random()
          , a = 360 * Math.random()
          , i = 35 * Math.random() * (Math.random() <= .5 ? -1 : 1)
          , r = this.mouseY - e / 2
          , o = this.mouseX - e / 2
          , s = Math.random() <= .5 ? -1 : 1
          , l = document.createElement("span");
        l.innerHTML = this.variants[Math.floor(Math.random() * this.variants.length)],
        l.classList.add("particle"),
        l.setAttribute("style", "\n      font-size: ".concat(e, "px;\n      top: ").concat(r, "px;\n      left: ").concat(o, "px;\n      transform: rotate(").concat(a, "deg);\n    ")),
        document.getElementById("content").appendChild(l),
        this.particles.push({
            direction: s,
            element: l,
            left: o,
            size: e,
            speedHorz: t,
            speedUp: n,
            spinSpeed: i,
            spinVal: a,
            top: r
        })
    }
}
}, {
key: "updateParticles",
value: function() {
    var e = this;
    this.particles.forEach((function(t) {
        t.left = t.left - t.speedHorz * t.direction,
        t.top = t.top - t.speedUp,
        t.speedUp = Math.min(t.size, t.speedUp - 1),
        t.spinVal = t.spinVal + t.spinSpeed,
        t.top >= Math.max(window.innerHeight, document.body.clientHeight) + t.size && (e.particles = e.particles.filter((function(e) {
            return e !== t
        }
        )),
        t.element.remove()),
        t.element.setAttribute("style", "\n        top: ".concat(t.top, "px;\n        left: ").concat(t.left, "px;\n        font-size: ").concat(t.size, "px;\n        transform:rotate(").concat(t.spinVal, "deg);\n      "))
    }
    ))
}
}])