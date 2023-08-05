### Haxball.py
---
#### Uses

**Index**
```py
import haxball.py
import asyncio

loop = asyncio.get_event_loop()
asyncio.ensure_future(Haxball("./bot.js").openroom())
loop.run_forever()
```

**bot.js**

```js
window.onHBLoaded = function () {

      const room = window.HBInit({
        roomName: "My room",
        maxPlayers: 16,
        public: true,
        noPlayer: true,
        token: "TOKEN"// Token: https://www.haxball.com/headlesstoken
      })
      room.setDefaultStadium("Big");
      room.setScoreLimit(5);
      room.setTimeLimit(0);
      function updateAdmins() {
        var players = room.getPlayerList();
        if ( players.length == 0 ) return; 
        if ( players.find((player) => player.admin) != null ) return; 
        room.setPlayerAdmin(players[0].id, true);
      };
      room.onPlayerJoin = function(player) {
        updateAdmins();
      };
      room.onPlayerLeave = function(player) {
        updateAdmins();
      }

/**END CODE */

if (typeof window.HBInit === 'function')
      window.onHBLoaded()

}
```