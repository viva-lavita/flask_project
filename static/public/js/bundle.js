$(function() {

    var ANGLE = 38.8;

    RM.STORE = (function () {
        var module = {},
            cacheDOM = {},
            cacheDATA = {};

        module.dom = {
            get: function(selector) {
                return cacheDOM[selector] || (cacheDOM[selector] = $(selector));
            },
            clear: function(selector) {
                selector == null ? cacheDOM = [] : cacheDOM[selector] = null;
            }
        };

        module.dom.d = $(document);
        module.dom.w = $(window);
        module.dom.b = $('body');

        module.data = {
            set: function(key, value) {
                cacheDATA[key] = value;
            },
            get: function(key) {
                return cacheDATA[key];
            },
            clear: function(key) {
                key == null ? cacheDATA = [] : cacheDATA[key] = null;
            }
        };

        return module;
    })();

    RM.STORE.data.set('wW', RM.STORE.dom.w.width());
    RM.STORE.data.set('wH', RM.STORE.dom.w.height());

    RM.STORE.dom.w.on('resize', function() {
        var self = $(this);

        RM.STORE.data.set('wW', self.width());
        RM.STORE.data.set('wH', self.height());

        RM.STORE.dom.d.trigger('rm.resize');
    });

    RM.page = (function() {
        var module = {},
            BC = 'b-page',
            page = $('.' + BC),
            first = $('.' + BC + '__first'),
            moveLeft = $('.' + BC + '__left', page),
            moveCenter = $('.' + BC + '__center', page),
            moveRight = $('.' + BC + '__right', page),
            moveCenterWidth = 600;

        function setPositionPort(e) {
            var offsetX = e.pageX,
                targetWidthLeft = 0,
                targetWidthRight = 0,
                deltaWidth,
                deltaY,
                boundaryLeft = RM.STORE.data.get('wW') / 2 - moveCenterWidth / 2,
                boundaryRight = RM.STORE.data.get('wW') / 2  + moveCenterWidth / 2,
                boundaryLeftNew,
                boundaryRightNew;

            deltaY = e.pageY - RM.STORE.data.get('wH') / 2;
            deltaWidth = Math.abs(deltaY) / Math.tan(90 - ANGLE);

            if (deltaY < 0) {
                // верхняя часть
                boundaryLeftNew = boundaryLeft + deltaWidth;
                boundaryRightNew = boundaryRight + deltaWidth;
            } else {
                // нижняя часть
                boundaryLeftNew = boundaryLeft - deltaWidth;
                boundaryRightNew = boundaryRight - deltaWidth;
            }

            if (e.pageX < boundaryLeftNew) {
                targetWidthLeft = boundaryLeft - e.pageX;

                deltaY < 0
                    // верхняя часть
                    ? targetWidthLeft += deltaWidth
                    // нижняя часть
                    : targetWidthLeft -= deltaWidth;

                targetWidthLeft = Math.round(targetWidthLeft);
            }

            moveLeft.css({
                width: targetWidthLeft
            });

            if (e.pageX > boundaryRightNew) {
                targetWidthRight = e.pageX - boundaryRight;

                deltaY < 0
                    // верхняя часть
                    ? targetWidthRight -= deltaWidth
                    // нижняя часть
                    : targetWidthRight += deltaWidth;

                targetWidthRight = Math.round(targetWidthRight);
            }

            moveRight.css({
                width: targetWidthRight
            });
        };

        module.init = function() {
            first.on('mousemove', function(e) {
                setPositionPort(e);
            });
        };

        return module;
    })();

    RM.page.init();

    RM.slider = (function() {
        var module = {},
            BC = 'b-slider',
            // dom
            slider = $('.' + BC),
            points = $('.' + BC + '__point', slider),
            items = $('.' + BC + '__item', slider),
            // vars
            prev = 0,
            next = 0,
            min = 0,
            max = items.length - 1,
            timer;

        function bindEvents() {

            points.on('mouseup touchend', function(e) {
                var self = $(this),
                    index = points.index(self);

                e.preventDefault();
                stop();
                next = index;
                toggle();
            });

            start();
        };

        function toggle(callback) {
            points.eq(prev).removeClass(BC + '__point--active');
            points.eq(next).addClass(BC + '__point--active');
            items.eq(prev).removeClass(BC + '__item--active');
            items.eq(next).addClass(BC + '__item--active');
            prev = next;
            if (typeof callback === 'function') callback();
        };

        function next() {
            next = prev + 1;
            if (next > max) next = min;
            if (next < min) next = max;
            toggle();
        };

        function start() {
            timer = setInterval(next, 3000);
        };

        function stop() {
            clearInterval(timer);
            timer = null;
        };

        module.init = function() {
            bindEvents();
        };

        return module;
    })();

    RM.slider.init();
});