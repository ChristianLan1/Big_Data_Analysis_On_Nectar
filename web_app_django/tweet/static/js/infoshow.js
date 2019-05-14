var infoWin;
var tableDom;
var rcmWins =[];
/**
 * 封装便捷的撞题
 * @param {AMap.Map} map
 * @param {Array} event
 * @param {Object} content
 */


function openInfoWin(map, event, content) {
    if (!infoWin) {
        infoWin = new AMap.InfoWindow({
            isCustom: true,  //使用自定义窗体
            offset: new AMap.Pixel(70, -10),
        });
    }

    var x = event.offsetX;
    var y = event.offsetY;
    var lngLat = map.containerToLngLat(new AMap.Pixel(x, y));
    // console.log(lngLat)

    if (!tableDom) {
        let infoDom = document.createElement('div');
        infoDom.className = 'window_info';
        tableDom = document.createElement('table');
        infoDom.appendChild(tableDom);
        infoWin.setContent(infoDom);
    }

    var trStr = '';
    for (var name in content) {
        var val = content[name];
        trStr += 
            '<tr>' +
                '<td class="label">' + name + '</td>' +
                '<td>&nbsp;</td>' +
                '<td class="content">' + val + '</td>' +
            '</tr>'
    }

    tableDom.innerHTML = trStr;
    infoWin.open(map, lngLat);
}

function closeInfoWin() {
    if (infoWin) {
        infoWin.close();
    }
}

function showRcmWin(map,points){
    var coor;
    var name;
    if(points.length > 0){
        for(city in points){
            coor = points[city]["center"].split(',')
            name = points[city]["name"]
            var rcmWin = new AMap.Marker({
                position:coor,
                content: "<div class = 'marker_wrap' ><div class='marker_label'><p>" +name + "</p></div></div>",
                offset: new AMap.Pixel(-5, -35),
            });
            rcmWins.push(rcmWin)
            
        }
        map.getMap().add(rcmWins)
    }
    return rcmWins
}

function closeRcmWin(map,rcmWins){
    rcmWins.forEach(marker => {
        map.remove(marker);
    });
    rcmWins = []
}