from django.shortcuts import render


def special_characters_view(request):
    special_characters = "૱┯┰┱┲❗►◄ĂăǕǖꞀ¤Ð¢℥Ω℧Kℶℷℸⅇ⅊⚌⚍⚎⚏⚭⚮⌀⏑⏒⏓⏔⏕⏖⏗⏘⏙⏠⏡⏦ᶀᶁᶂᶃᶄᶆᶇᶈᶉᶊᶋᶌᶍᶎᶏᶐᶑᶒᶓᶔᶕᶖᶗᶘᶙᶚᶸᵯᵰᵴᵶᵹᵼᵽᵾᵿ  ‎‏ ⁁⁊ ⁪⁫⁬⁭⁮⁯⸜⸝¶¥£" \
                         "⅕⅙⅛⅔⅖⅗⅘⅜⅚⅐⅝↉⅓⅑⅒⅞←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖" \
                         "⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇨⇩⇪⇧⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿⟰⟱⟲⟳⟴⟵⟶⟷⟸⟹⟺⟻⟼⟽⟾⟿⤀⤁⤂⤃⤄⤅⤆⤇⤈⤉⤊⤋⤌⤍" \
                         "⤎⤏⤐⤑⤒⤓⤔⤕⤖⤗⤘⤙⤚⤛⤜⤝⤞⤟⤠⤡⤢⤣⤤⤥⤦⤧⤨⤩⤪⤫⤬⤭⤮⤯⤰⤱⤲⤳⤴⤵⤶⤷⤸⤹⤺⤻⤼⤽⤾⤿⥀⥁⥂⥃⥄⥅⥆⥇⥈⥉⥊⥋⥌⥍⥎⥏⥐⥑" \
                         "⥒⥓⥔⥕⥖⥗⥘⥙⥚⥛⥜⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦⥧⥨⥩⥪⥫⥬⥭⥮⥯⥰⥱⥲⥳⥴⥵⥶⥷⥸⥹⥺⥻⥼⥽⥾⥿➔➘➙➚➛➜➝➞➝➞➟➠➡➢➣➤➥➦➧➨➩➩➪➫➬➭➮➯" \
                         "➱➲➳➴➵➶➷➸➹➺➻➼➽➾⬀⬁⬂⬃⬄⬅⬆⬇⬈⬉⬊⬋⬌⬍⬎⬏⬐⬑☇☈⏎⍃⍄⍅⍆⍇⍈⍐⍗⍌⍓⍍⍔⍏⍖♾⎌☊☋☌☍⌃⌄⌤⌅⌆⌇⚋⚊⌌⌍⌎⌏⌐⌑⌔⌕⌗⌙⌢⌣⌯⌬⌭⌮⌖⌰⌱" \
                         "⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⍯⍰⌽⌾⌿⍀⍁⍂⍉⍊⍋⍎⍏⍑⍒⍕⍖⍘⍙⍚⍛⍜⍝⍞⍠⍟⍡⍢⍣⍤⍥⍨⍩⍦⍧⍬⍿⍪⍮⍫⍱⍲⍭⍳⍴⍵⍶⍷⍸⍹⍺⍼⍽⍾⎀⎁⎂⎃⎄⎅⎆⎉⎊⎋⎍⎎⎏⎐⎑⎒⎓⎔⎕" \
                         "⏣⌓⏥⏢⎖⎲⎳⎴⎵⎶⎸⎹⎺⎻⎼⎽⎾⎿⏀⏁⏂⏃⏄⏅⏆⏇⏈⏉⏉⏋⏌⏍⏐⏤⏚⏛Ⓝℰⓦ!   ⌘«»‹›‘’“”„‚❝❞£¥€$¢¬¶@§®©™°×π±√‰Ω∞≈÷~≠¹²³½" \
                         "¼¾‐–—|⁄\[\]{}†‡…·•●⌥⌃⇧↩¡¿‽⁂∴∵◊※←→↑↓☜☞☝☟✔★☆♺☼☂☺☹☃✉✿✄✈✌✎♠♦♣♥♪♫♯♀♂αßÁáÀàÅåÄäÆæÇçÉéÈèÊêÍíÌì" \
                         "ÎîÑñÓóÒòÔôÖöØøÚúÙùÜüŽž₳฿￠€₡¢₢₵₫￡£₤₣ƒ₲₭₥₦₱＄$₮₩￦¥￥₴₰¤៛₪₯₠₧₨௹﷼㍐৲৳~ƻƼƽ¹¸¬¨ɂǁ¯Ɂǂ¡´°ꟾ¦}{|\.," \
                         "·\]\)\[/_\¿º§\"\*\-\+\(!&%$¼¾½¶©®@ẟⱿ`Ȿ^꜠꜡ỻ'=:;<ꞌꞋ꞊ꞁꞈ꞉>?÷ℾℿ℔℩℉⅀℈þðÞµªꝋꜿꜾⱽⱺⱹⱷⱶⱵⱴⱱⱰⱦȶȴȣȢȡȝȜțȋȊ" \
                         "ȉȈǯǮǃǀƿƾƺƹƸƷƲưƪƣƢƟƛƖƕƍſỽ⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸔⸕▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙" \
                         "⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇" \
                         "⧅⧄⍁⍂⟡⧉○◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑╰╮╭╯⌒╳✕╱╲⧸⧹⌓◦❖✖" \
                         "✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃ ‒\-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥" \
                         "┦┧┨┩┪┫┬┭┮┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬⌞⌟⌜⌝⌊⌋⌉⌈⌋₯ἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑ" \
                         "ἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸ" \
                         "όὺύὼώᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙ" \
                         "ῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγ" \
                         "δεζηθικλμνξοπρςστυφχψωϊϋόύώϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿⒶⓐ⒜ẠạẢảḀḁÂÃǍǎẤ" \
                         "ấẦầẨẩȂȃẪẫẬậÀÁẮắẰằẲẳẴẵẶặĀāĄąǞȀȁÅǺǻÄäǟǠǡâáåãàẚȦȧȺÅⱥÆæǼǢǣⱯꜲꜳꜸꜺⱭꜹꜻª℀⅍℁Ⓑⓑ⒝ḂḃḄḅḆḇƁɃƀƃƂƄƅℬⒸ" \
                         "ⓒ⒞ḈḉĆćĈĉĊċČčÇçƇƈȻȼℂ℃ℭƆ℅℆℄ꜾꜿⒹⓓ⒟ḊḋḌḍḎḏḐḑḒḓĎďƊƋƌƉĐđȡⅅⅆǱǲǳǄǅǆȸⒺⓔ⒠ḔḕḖḗḘḙḚḛḜḝẸẹẺẻẾếẼẽỀ" \
                         "ềỂểỄễỆệĒēĔĕĖėĘęĚěÈèÉéÊêËëȄȅȨȩȆȇƎⱸɆℇℯ℮ƐℰƏǝⱻɇⒻⓕ⒡ḞḟƑƒꜰℲⅎꟻℱ℻Ⓖⓖ⒢ƓḠḡĜĝĞğĠġĢģǤǥǦǧǴℊ⅁ǵⒽⓗ⒣ḢḣḤḥḦḧ" \
                         "ḨḩḪḫẖĤĥȞȟĦħⱧⱨꜦℍǶℏℎℋℌꜧⒾⓘ⒤ḬḭḮḯĲĳìíîïÌÍÎÏĨĩĪīĬĭĮįıƗƚỺǏǐⅈⅉℹℑℐⒿⓙ⒥ĴĵȷⱼɈɉǰⓀⓚ⒦ḰḱḲḳḴḵĶķƘƙꝀꝁꝂꝃꝄꝅǨǩⱩⱪĸ" \
                         "Ⓛⓛ⒧ḶḷḸḹḺḻḼḽĹĺĻļĽİľĿŀŁłỈỉỊịȽⱠꝈꝉⱡⱢꞁℒǇǈǉ⅃⅂ℓȉȈȊȋⓂⓜ⒨ḾḿṀṁṂṃꟿꟽⱮƩƜℳⓃⓝ⒩ṄṅṆṇṈṉṊṋŃńŅņŇňǸǹŊƝñŉÑȠƞŋǊǋ" \
                         "ǌȵℕ№ṌṍṎṏṐṑṒṓȪȫȬȭȮȯȰȱǪǫǬǭỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợƠơŌōŎŏŐőÒÓÔÕÖǑȌȍȎȏŒœØǾꝊǽǿℴ⍥⍤Ⓞⓞ⒪òóôõöǒøꝎ" \
                         "ꝏⓅⓟ⒫℗ṔṕṖṗƤƥⱣℙǷꟼ℘Ⓠⓠ⒬Ɋɋℚ℺ȹⓇⓡ⒭ŔŕŖŗŘřṘṙṚṛṜṝṞṟȐȑȒȓɍɌƦⱤ℞Ꝛꝛℜℛ℟ℝⓈⓢ⒮ṠṡṢṣṤṥṦṧṨṩŚśŜŝŞşŠšȘșȿꜱƧƨẞß" \
                         "ẛẜẝ℠Ⓣⓣ⒯ṪṫṬṭṮṯṰṱŢţŤťŦŧƬƮẗȚȾƫƭțⱦȶ℡™Ⓤⓤ⒰ṲṳṴṵṶṷṸṹṺṻỤỦủỨỪụứỬửừữỮỰựŨũŪūŬŭŮůŰűǙǚǗǘǛǜŲųǓǔȔȕÛûȖȗÙùÜ" \
                         "üƯúɄưƲƱⓋⓥ⒱ṼṽṾṿỼɅ℣ⱱⱴⱽⓌⓦ⒲ẀẁẂẃẄẅẆẇẈẉŴŵẘⱲⱳⓍⓧ⒳ẊẋẌẍℵ×Ⓨⓨ⒴ẎẏỾỿẙỲỳỴỵỶỷỸỹŶŷƳƴŸÿÝýɎɏȲƔ⅄ȳℽⓏⓩ⒵ẐẑẒẓẔ" \
                         "ẕŹźŻżŽžȤȥⱫⱬƵƶɀℨℤ⟀⟁⟂⟃⟄⟇⟈⟉⟊⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥⟦⟧⟨⟩⟪⟫⦀⦁⦂⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⦙⦚⦛⦜⦝⦞⦟⦠⦡" \
                         "⦢⦣⦤⦥⦦⦧⦨⦩⦪⦫⦬⦭⦮⦯⦰⦱⦲⦳⦴⦵⦶⦷⦸⦹⦺⦻⦼⦽⦾⦿⧀⧁⧂⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟⧡⧢⧣⧤⧥⧦⧧⧨⧩⧪⧫" \
                         "⧬⧭⧮⧯⧰⧱⧲⧳⧴⧵⧶⧷⧸⧹⧺⧻⧼⧽⧾⧿∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆" \
                         "≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠" \
                         "⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬" \
                         "⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿✕✖✚◀▶❝❞★☆☼☂☺☹✄✈✌✎♪♫☀☁☔⚡❆☽☾✆✔☯☮☠⚑☬✄✏♰✡✰✺⚢⚣♕♛♚♬ⓐⓑⓒⓓ↺↻⇖⇗⇘⇙⟵⟷⟶⤴⤵⤶" \
                         "⤷➫➬€₤＄₩₪⟁⟐◆⎔░▢⊡▩⟡◎◵⊗❖ΩβΦΣΞ⟁⦻⧉⧭⧴∞≌⊕⋍⋰⋱✖⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾ᴕ⸨⸩❪❫⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓" \
                         "⒔⒕⒖⒗⒘⒙⒚⒛⓪①②③④⑤⑥⑦⑧⑨⑩➀➁➂➃➄➅➆➇➈➉⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⓿❶❷❸❹❺❻❼❽❾❿➊➋➌➍➎➏➐➑➒➓⓫⓬⓭⓮⓯⓰⓱⓲" \
                         "⓳⓴⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇ᶅᶛᶜᶝᶞᶟᶠᶡᶢᶣᶤᶥᶦᶧᶨᶩᶪᶫᶬᶭᶮᶯᶰᶱᶲᶳᶴᶵᶶᶷᶹᶺᶻᶼᶽᶾᶿᴀᴁᴂᴃᴄᴅᴆᴇᴈᴉᴊᴋᴌᴍᴎᴏᴐᴑ" \
                         "ᴒᴓᴔᴕᴖᴗᴘᴙᴚᴛᴜᴝᴞᴟᴠᴡᴢᴣᴤᴥᴦᴧᴨᴩᴪᴫᴬᴭᴮᴯᴰᴱᴲᴳᴴᴵᴶᴷᴸᴹᴺᴻᴼᴽᴾᴿᵀᵁᵂᵃᵄᵅᵆᵇᵈᵉᵊᵋᵌᵍᵎᵏᵐᵑᵒᵓᵔᵕᵖᵗᵘᵙᵚᵛᵜᵝᵞᵟᵠᵡᵢᵣᵤᵥᵦᵧᵨᵩᵪᵫᵬᵭᵮᵱᵲᵳᵵ" \
                         "ᵷᵸᵺᵻ ᷋ ᷌ ᷍ ᷎ ᷏ ᷓ ᷔ ᷕ ᷖ ᷗ ᷘ ᷙ ᷛ ᷜ ᷝ ᷞ ᷟ ᷠ ᷡ ᷢ ᷣ ᷤ ᷥ ᷦ‘’‛‚“”„‟«»‹›Ꞌ\"❛❜❝❞<>@‧¨․꞉:⁚⁝⁞‥…⁖⸪⸬⸫⸭⁛⁘⁙⁏;⦂⁃‐ ‒\-–⎯—―" \
                         "_⁓⸛⸞⸟ⸯ¬/\⁄\⁄|⎜¦‖‗†‡·•⸰°‣⁒%‰‱&⅋§÷\+±=꞊′″‴⁗‵‶‷‸\*⁑⁎⁕※⁜⁂!‼¡?¿⸮⁇⁉⁈‽⸘¼½¾²³©®™℠℻℅℁⅍℄¶⁋❡⁌⁍⸖⸗⸚⸓\(" \
                         "\)\[\]{}⸨⸩❨❩❪❫⸦⸧❬❭❮❯❰❱❴❵❲❳⦗⦘⁅⁆〈〉⏜⏝⏞⏟⸡⸠⸢⸣⸤⸥⎡⎤⎣⎦⎨⎬⌠⌡⎛⎠⎝⎞⁀⁔‿⁐‾⎟⎢⎥⎪ꞁ⎮⎧⎫⎩⎭⎰⎱✈☀☼☁☂☔⚡❄❅❆☃☉☄★☆☽☾⌛⌚" \
                         "☇☈⌂⌁✆☎☏☑✓✔⎷⍻✖✗✘☒✕☓☕♿✌☚☛☜☝☞☟☹☺☻☯⚘☮✝⚰⚱⚠☠☢⚔⚓⎈⚒⚑⚐☡❂⚕⚖⚗✇☣⚙☤⚚⚛⚜☥☦☧☨☩†☪☫☬☭✁✂✃✄✍✎✏✐✑✒✉✙✚✜✛♰♱✞✟✠✡☸" \
                         "✢✣✤✥✦✧✩✪✫✬✭✮✯✰✲✱✳✴✵✶✷✸✹✺✻✼✽✾❀✿❁❃❇❈❉❊❋⁕☘❦❧☙❢❣♀♂⚢⚣⚤⚦⚧⚨⚩☿♁⚯♔♕♖♗♘♙♚♛♜♝♞♟☖☗♠♣♦♥❤❥♡♢♤♧⚀⚁⚂⚃⚄⚅" \
                         "⚇⚆⚈⚉♨♩♪♫♬♭♮♯⌨⏏⎗⎘⎙⎚⌥⎇⌘⌦⌫⌧♲♳♴♵♶♷♸♹♺♻♼♽⁌⁍⎌⌇⌲⍝⍟⍣⍤⍥⍨⍩⎋♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓⏚⏛| | | || | | | | ||"

    return render(request, 'utils/pages/special_characters.html', {'special_characters': special_characters})
