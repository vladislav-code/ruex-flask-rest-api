ymaps.ready(init);

let center = [55.75502356900459,37.50924450000006];

function init() {
    let map = new ymaps.Map('map', {
        center: center,
        zoom: 16,
        controls: ['routePanelControl']
    });

    let control = map.controls.get('routePanelControl');

    let location = ymaps.geolocation.get();

    location.then(function(res) {
        let locationText = res.geoObjects.get(0).properties.get('text');
        control.routePanel.state.set({
            type: 'masstransit',
            fromEnabled: true,
            toEnabled: false,
            to: `Береговой проезд 5Ак1 БЦ "Фили Град" Москва, Россия, 121087`,
            from: locationText
        })
    })

    let placemarkOwn = new ymaps.Placemark(center, {
        balloonContent: `
        
            <div class="balloon">
            
                <div class="balloon_address">Береговой проезд 5Ак1 <br>БЦ "Фили Град" <br>Москва, Россия, 121087</div>
                <div class="balloon contacts">
                
                    <a href="tel:+74956629967">+7 (495) 662-99-67 (доб.9010)</a>
                    <br>
                    <a href="tel:+79261113316">+7 (926) 111-33-16</a>

                </div>

            </div>

        `
    }, {
        iconLayout: 'default#image',
        iconImageHref: '/images/marker.png',
        iconImageSize: [40, 40],
        iconImageOffset: [-15, -35]
    });

    map.geoObjects.add(placemarkOwn);
}
