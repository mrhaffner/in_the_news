from bs4 import BeautifulSoup

# takes in a datetime
# finds the appropriate folder at that datetime
# for each xml file in that folder, parses the xml rss file
# saves title, url, pubdate, and author? for each article in feed to db/or file? with specified datetime/website
# key can be url? or title+website?


# def save_xml_date(datetime)
    # convert datetime to path
    # loop over files in path
        # parse_xml(filepath)
        # save_to_whatver

#def soup_from_filepath(file_path):
    #with open(file_path) as fp:
        #soup = BeautifulSoup(fp, 'lxml')

# throws i/o error
def parse_soup(soup):
    items = soup.find_all('item')

    articles = []

    for item in items:
        title = item.title.get_text()
        pubDate = item.pubDate.get_text()
        url = item.link.get_text()
        author = get_author(item)
        # id is hashed url
        article = {
            'title': title,
            'pubDate': pubDate,
            'url': url,
            'author': author,
        }

        articles.append(article)

    return articles


def get_author(item):
    author = item.creator.get_text()

    if author == '':
        author = item.author.get_text()

    return author
# dc:creator
# author
# 

test = '''
<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	>

<channel>
	<title>The Gateway Pundit</title>
	<atom:link href="https://www.thegatewaypundit.com/feed/?Mozilla%2F5_0_%28Windows_NT_10_0%3B_Win64%3B_x64%29_AppleWebKit%2F537_36_%28KHTML%2C_like_Gecko%29_Chrome%2F91_0_4472_124_Safari%2F537_36" rel="self" type="application/rss+xml" />
	<link>https://www.thegatewaypundit.com</link>
	<description>Where Hope Finally Made a Comeback</description>
	<lastBuildDate>Tue, 03 May 2022 17:55:49 +0000</lastBuildDate>
	<language>en-US</language>
	<sy:updatePeriod>
	hourly	</sy:updatePeriod>
	<sy:updateFrequency>
	1	</sy:updateFrequency>
	<generator>https://wordpress.org/?v=5.8.4</generator>

<image>
	<url>https://www.thegatewaypundit.com/wp-content/uploads/tgpfavicon-150x150.png</url>
	<title>The Gateway Pundit</title>
	<link>https://www.thegatewaypundit.com</link>
	<width>32</width>
	<height>32</height>
</image> 
	<item>
		<title>CDC Used Phone Location Data to Monitor Churches and Schools to Determine Whether Americans Followed Covid Lockdown Orders</title>
		<link>https://www.thegatewaypundit.com/2022/05/cdc-used-phone-location-data-monitor-churches-schools-determine-whether-americans-followed-covid-lockdown-orders/</link>
		
		<dc:creator><![CDATA[Cristina Laila]]></dc:creator>
		<pubDate>Tue, 03 May 2022 17:55:00 +0000</pubDate>
				<category><![CDATA[Uncategorized]]></category>
		<guid isPermaLink="false">https://www.thegatewaypundit.com/?p=729574</guid>

					<description><![CDATA[<p>The Centers for Disease Control and Prevention used phone location data to track millions Americans in 2021. The CDC monitored curfew zones, churches, schools, neighbor-to-neighbor visits and trips to pharmacies through SafeGraph, a controversial data broker. The CDC purchased the phone data and used Covid-19 as an excuse to buy the data more quickly and&#8230;</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/cdc-used-phone-location-data-monitor-churches-schools-determine-whether-americans-followed-covid-lockdown-orders/">CDC Used Phone Location Data to Monitor Churches and Schools to Determine Whether Americans Followed Covid Lockdown Orders</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></description>
										<content:encoded><![CDATA[<p><img loading="lazy" class="alignnone size-full wp-image-634313" src="https://www.thegatewaypundit.com/wp-content/uploads/22A60C74-7289-4C8C-8445-2E8FE59E0E3A.jpeg" alt="" width="1264" height="712" srcset="https://www.thegatewaypundit.com/wp-content/uploads/22A60C74-7289-4C8C-8445-2E8FE59E0E3A.jpeg 1264w, https://www.thegatewaypundit.com/wp-content/uploads/22A60C74-7289-4C8C-8445-2E8FE59E0E3A-105x59.jpeg 105w" sizes="(max-width: 1264px) 100vw, 1264px" /></p>
<p>The Centers for Disease Control and Prevention used phone location data to track millions Americans in 2021.</p>
<p>The CDC monitored curfew zones, churches, schools, neighbor-to-neighbor visits and trips to pharmacies through SafeGraph, a controversial data broker.</p>
<p>The CDC purchased the phone data and used Covid-19 as an excuse to buy the data more quickly and in larger quantities according to documents exclusively obtained by Motherboard through a FOIA request.</p>
<p>The CDC used the data to determine whether Americans were complying with Covid lockdown orders.</p>
<p>Motherboard <a href="https://www.vice.com/en/article/m7vymn/cdc-tracked-phones-location-data-curfews" target="_blank" rel="noopener">reported</a>:</p>
<blockquote><p>The documents reveal the expansive plan the CDC had last year to use location data from a highly controversial data broker. SafeGraph, the company the CDC paid $420,000 for access to one year of data to, includes Peter Thiel and the former head of Saudi intelligence among its investors. Google <a href="https://www.vice.com/en/article/5db4ad/google-bans-safegraph-former-saudi-intelligence">banned the company from the Play Store</a> in June.</p>
<p>The Centers for Disease Control and Prevention (CDC) bought access to location data harvested from tens of millions of phones in the United States to perform analysis of compliance with curfews, track patterns of people visiting K-12 schools, and specifically monitor the effectiveness of policy in the Navajo Nation, according to CDC documents obtained by Motherboard. The documents also show that although the CDC used COVID-19 as a reason to buy access to the data more quickly, it intended to use it for more general CDC purposes.</p>
<p>The CDC used the data for monitoring curfews, with the documents saying that SafeGraph’s data “has been critical for ongoing response efforts, such as hourly monitoring of activity in curfew zones or detailed counts of visits to participating pharmacies for vaccine monitoring.” The documents date from 2021.</p>
<p>Motherboard obtained the documents through a Freedom of Information Act (FOIA) request with the CDC.</p>
<p>The documents contain a long list of what the CDC describes as 21 different “potential CDC use cases for data.” They include:</p>
<p>&nbsp;</p></blockquote>
<ul>
<li>
<blockquote><p>“Track patterns of those visiting K-12 schools by the school and compare to 2019; compare with epi metrics [Environmental Performance Index] if possible.”</p></blockquote>
</li>
<li>
<blockquote><p>“Examination of the correlation of mobility patterns data and rise in COVID-19 cases [&#8230;] Movement restrictions (Border closures, inter-regional and nigh curfews) to show compliance.”</p></blockquote>
</li>
<li>
<blockquote><p>“Examination of the effectiveness of public policy on [the] Navajo Nation.”</p></blockquote>
</li>
</ul>
<p>Read the full report by Motherboard <a href="https://www.vice.com/en/article/m7vymn/cdc-tracked-phones-location-data-curfews" rel="noopener" target="_blank">here</a>.</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/cdc-used-phone-location-data-monitor-churches-schools-determine-whether-americans-followed-covid-lockdown-orders/">CDC Used Phone Location Data to Monitor Churches and Schools to Determine Whether Americans Followed Covid Lockdown Orders</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></content:encoded>
					
		
		
		<enclosure url="http://www.thegatewaypundit.com/wp-content/uploads/22A60C74-7289-4C8C-8445-2E8FE59E0E3A.jpeg" length="199302" type="image/jpeg" />	</item>
		<item>
		<title>Flashback: In 1982 Joe Biden Voted for Constitutional Amendment to Overturn Roe v Wade and Make It a State Issue</title>
		<link>https://www.thegatewaypundit.com/2022/05/flashback-1982-joe-biden-voted-constitutional-amendment-overturn-roe-v-wade-make-states-issue/</link>
		
		<dc:creator><![CDATA[Jim Hoft]]></dc:creator>
		<pubDate>Tue, 03 May 2022 17:34:00 +0000</pubDate>
				<category><![CDATA[Uncategorized]]></category>
		<guid isPermaLink="false">https://www.thegatewaypundit.com/?p=729590</guid>

					<description><![CDATA[<p>&#8220;When Joe Biden Voted to Let States Overturn Roe v. Wade&#8221; &#8212;New York Times The US Supreme Court reportedly voted to END Roe v Wade in a DRAFT OPINION by Justice Samuel Alito according to a report leaked to Politico on Monday night. The draft opinion was leaked to the press – something that is unprecedented. Of&#8230;</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/flashback-1982-joe-biden-voted-constitutional-amendment-overturn-roe-v-wade-make-states-issue/">Flashback: In 1982 Joe Biden Voted for Constitutional Amendment to Overturn Roe v Wade and Make It a State Issue</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></description>
										<content:encoded><![CDATA[<p><img loading="lazy" class="alignnone size-full wp-image-729597" data-src="https://www.thegatewaypundit.com/wp-content/uploads/biden-nyt-abortion-states-.jpg" alt="" width="661" height="576" /><br />
<span style="font-size: 10pt;"><em>&#8220;When Joe Biden Voted to Let States Overturn Roe v. Wade&#8221; &#8212;<a href="http://When Joe Biden Voted to Let States Overturn Roe v. Wade">New York Times</a></em></span></p>
<p>The US Supreme Court reportedly<a href="https://www.thegatewaypundit.com/2022/05/breaking-supreme-court-vote-end-roe-v-wade-draft-opinion-justice-samuel-alito/"> voted to END Roe v Wade in a DRAFT OPINION</a> by Justice Samuel Alito according to a report leaked to Politico on Monday night.</p>
<p>The draft opinion was leaked to the press – something that is unprecedented. Of course, most assume the leaker is a liberal clerk who hopes to change the outcome of the case.</p>
<p>Joe Biden <a href="https://www.thegatewaypundit.com/2022/05/biden-releases-statement-supreme-courts-decision-draft-end-roe-v-wade-doesnt-mention-unprecedented-leak-press/">responded to the leaked decision</a> Tuesday morning. His handlers released a statement.</p>
<p><img loading="lazy" class="alignnone size-full wp-image-729539" data-src="https://www.thegatewaypundit.com/wp-content/uploads/FR1ncFMXoAAuSN8-scaled.jpg" alt="" width="1812" height="2560" /></p>
<p><strong>But back in 1982, Joe Biden voted for a constitutional amendment to overturn Roe v Wade and make it a state issue.</strong></p>
<p><em>Via David Harsanyi</em></p>
<blockquote class="twitter-tweet">
<p dir="ltr" lang="en">In 1982 Joe Biden proposed a constitutional amendment that would overturn Roe v. Wade and allow states to choose their own policies on abortion.</p>
<p>— David Harsanyi (@davidharsanyi) <a href="https://twitter.com/davidharsanyi/status/1521490506525589504">May 3, 2022</a></p></blockquote>
<p><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script></p>
<blockquote class="twitter-tweet">
<p dir="ltr" lang="en">In 1994, Biden wrote a letter to a constituent bragging that he has voted against abortion funding on 50 separate occasions. <a href="https://t.co/XiVbeBM32x">https://t.co/XiVbeBM32x</a></p>
<p>— David Harsanyi (@davidharsanyi) <a href="https://twitter.com/davidharsanyi/status/1521490773421789184">May 3, 2022</a></p></blockquote>
<p><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script></p>
<p>Via <a href="https://www.catholicleague.org/bidens-evolving-views-on-abortion/">The Catholic League</a>:</p>
<blockquote><p>Joe Biden entered the senate in 1973, the same year the Supreme Court legalized abortion in its Roe v. Wade decision. He has evolved from being strongly pro-life to rabidly pro-abortion. Here is a list of his changing positions.</p>
<p>1974: A year after Roe v. Wade was decided, he said the ruling had gone “too far” and that a woman seeking an abortion should not have the “sole right to say what should happen to her body.”</p>
<p>1976: He votes for the “Hyde Amendment” which bans federal funding of abortions.</p>
<p>1981: He introduces the “Biden Amendment” which prohibits foreign-aid funding of biomedical research involving abortion.</p>
<p>1982: He votes for a constitutional amendment allowing states to overturn Roe v. Wade.</p>
<p>1983: He votes against a constitutional amendment allowing states to overturn Roe v. Wade.</p>
<p>1984: He votes for the Mexico City Policy which bans federal funding for abortions.</p>
<p>1987: He becomes chairman of the Senate Judiciary Committee and leads the fight against Supreme Court nominee Judge Robert Bork, whom he said was opposed to Roe v. Wade.</p></blockquote>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/flashback-1982-joe-biden-voted-constitutional-amendment-overturn-roe-v-wade-make-states-issue/">Flashback: In 1982 Joe Biden Voted for Constitutional Amendment to Overturn Roe v Wade and Make It a State Issue</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></content:encoded>
					
		
		
		<enclosure url="http://www.thegatewaypundit.com/wp-content/uploads/biden-nyt-abortion-states-.jpg" length="62843" type="image/jpeg" />	</item>
		<item>
		<title>WATCH: Special Ed Teacher Choked 7-Year-Old For Refusing To Wear Mask</title>
		<link>https://www.thegatewaypundit.com/2022/05/watch-special-ed-teacher-choked-7-year-old-refusing-wear-mask/</link>
		
		<dc:creator><![CDATA[Alicia Powe]]></dc:creator>
		<pubDate>Tue, 03 May 2022 17:15:00 +0000</pubDate>
				<category><![CDATA[Uncategorized]]></category>
		<guid isPermaLink="false">https://www.thegatewaypundit.com/?p=727784</guid>

					<description><![CDATA[<p>A Lowry Elementary School special education teacher is seen assaulting and choking a 7-year-old boy who refused to wear a mask in surveillance footage obtained by The Gateway Pundit. As The Gateway Pundit reported, Lowry Elementary school officials in Denver, Colorado persistently harassed Anthony Chavez and his son Chase for refusing to allow Chase to wear a&#8230;</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/watch-special-ed-teacher-choked-7-year-old-refusing-wear-mask/">WATCH: Special Ed Teacher Choked 7-Year-Old For Refusing To Wear Mask</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></description>
										<content:encoded><![CDATA[<p><img loading="lazy" class="size-full wp-image-729560 aligncenter" data-src="https://www.thegatewaypundit.com/wp-content/uploads/chase-choked-.jpg" alt="" width="796" height="490" /></p>
<p>A Lowry Elementary School special education teacher is seen assaulting and choking a 7-year-old boy who refused to wear a mask in surveillance footage obtained by The Gateway Pundit.</p>
<p><a href="https://www.thegatewaypundit.com/2022/02/single-father-put-house-arrest-school-guards-frame-allegedly-assault-locked-7-year-old-son-gym-not-wearing-face-mask/" target="_blank" rel="noopener">As <em>The Gateway Pundit</em> reported</a>, Lowry Elementary school officials in Denver, Colorado persistently harassed Anthony Chavez and his son Chase for refusing to allow Chase to wear a mask at school after the governor rescinded the mask mandate for indoor venues.</p>
<p>“Chase’s teacher began putting window screens around him and around his desk,” Chavez, a 42-year-old single father told <em>TGP</em>. “I instructed Chase to kindly put the windows next to the trash and not allow himself to be separated. They were attempting to have him sit six feet away from the other children while they were in their ‘numbers corner.’ They made him walk in front of the other kids as they walked through the halls to art class. I found out and I said, ‘That is not going to happen anymore and put a stop to it.’”</p>
<p>“I sent them an email instructing them to stop going against my parental directive – my instructive was clear, ‘Do not try to incentivize or try to manipulate my son to wear a mask for any reason.’ But he continued to do it,” Chavez said.</p>
<p>The interim assistant principal even attempted to bribe Chase into wearing a mask by “offering bags of potato chips, candy and extra recess” if he complied.</p>
<p>On February 18, Anthony Chavez received a call from the principal asking him to pick Chase up from school. A student who regularly began bullying Chase after he stopped wearing a mask in class destroyed Chase’s Lego creation during recess.</p>
<p>Chase claimed <a href="https://www.facebook.com/susan.rayburn.18/?show_switched_toast=0&amp;show_invite_to_follow=0&amp;show_switched_tooltip=0&amp;show_podcast_settings=0&amp;show_community_transition=0&amp;show_community_review_changes=0" target="_blank" rel="noopener">Susan Rayburn, a special ed teacher</a>, grabbed him and choked him as she carried him across the room when he asked her to resolve the dispute. His father received a call from the principal telling him to pick Chase up early and that they were &#8220;required&#8221; to put him in a restraint hold.</p>
<p>&#8220;I couldn&#8217;t really breathe so I tried to stand up to have my neck breathe, but it was too hard,&#8221; the 7-year-old boy <a href="https://www.thegatewaypundit.com/2022/02/7-year-old-boy-allegedly-choked-put-restraint-hold-thrown-across-room-not-wearing-mask-school/" target="_blank" rel="noopener">told</a> his father following the incident. &#8220;I tried to stop her but I couldn&#8217;t.&#8221;</p>
<p><img loading="lazy" class="alignnone wp-image-727789" data-src="https://www.thegatewaypundit.com/wp-content/uploads/lowry2.jpg" alt="" width="755" height="469" /></p>
<p>Surveillance footage corroborates Chase&#8217;s account. In the footage, Rayburn grabs the boy, wraps his elbows around his neck and picks him up so that his feet are lifted from the ground and carries him in the chokehold across the school library in front of at least three other school administrators.</p>
<p><strong>WATCH</strong>:</p>
<p><iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" title="WATCH: Special Ed Teacher Chokes, Assaults 7 Year Old Boy for Refusing To Wear Mask" data-src="https://rumble.com/embed/v10429g/?pub=jon1d#?secret=bELyOguGab" data-secret="bELyOguGab" width="750" height="422" frameborder="0"></iframe></p>
<p>Neurologists have called for police to stop using restraint holds and neck restraints, <a href="https://www.verywellhealth.com/neurologists-viewpoint-police-use-of-neck-restraints-5094737" target="_blank" rel="noopener">warning</a> the blockage of blood flow to the brain through two pressure points on the neck and compression of airflow through the windpipe can be deadly.</p>
<p>“The whole importance of the blood flow itself is that the blood is what’s carrying the oxygen, so if you’re not getting blood up to the brain, you’re not getting oxygen to the brain,” says Jillian Berkman, MD, “The end result could still be the same as when you’re choking someone. Both chokeholds and strangleholds have the potential to be deadly.”</p>
<p>&#8220;If someone is on top of you, they’re not seeing signs of any of these, so there’s no way to know it is happening,&#8221; Berkman says. &#8220;In the case of immediate death, what likely happens is you experience cardiac arrest from not getting enough oxygen to the heart and the lungs. Having a large stroke can definitely lead to death, but that usually takes hours because the brain tissue will swell and then compress the area responsible for consciousness. People can also die of seizures, but that&#8217;s also rarer.&#8221;</p>
<p><img loading="lazy" class="" src="https://www.thegatewaypundit.com/wp-content/uploads/restraint.png" width="596" height="397" /></p>
<p>&nbsp;</p>
<p><a href="https://www.thegatewaypundit.com/2022/04/watch-suveillance-footage-confirms-school-guards-assaulted-framed-single-father-put-house-arrest-refusing-mask-7-year-old-son/" target="_blank" rel="noopener">Last month</a>, security guards employed with Lowry Elementary School were seen assaulting Anthony Chavez in surveillance footage obtained by the Gateway Pundit.</p>
<p>Chavez, who was <a href="https://www.thegatewaypundit.com/2022/02/single-father-put-house-arrest-school-guards-frame-allegedly-assault-locked-7-year-old-son-gym-not-wearing-face-mask/" target="_blank" rel="noopener">put on house arrest</a> following the assault and mandated to wear an ankle bracelet, claims the guards tried to blockade him from leaving school premises and walking back to his car in an effort to frame him with trespassing charges over his refusal to comply with the mask mandate.</p>
<p><iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" title="Guards Seen In Suveillance Footage Assaulting Single Father For Refusing To Mask 7-Year-Old Son" data-src="https://rumble.com/embed/vxcwjq/?pub=jon1d#?secret=kCzdUoLi3M" data-secret="kCzdUoLi3M" width="750" height="422" frameborder="0"></iframe></p>
<p>Chavez, who remains on house arrest while he fights trespassing and assault charges, has obtained counsel to sue Rayburn and Lowry Elementary school.</p>
<p>&#8220;My next immediate action is to file a civil suit against Susan Rayburn. She didn&#8217;t like that my son was the only one in the school not wearing a mask. These teachers were all sitting there watching the kid bully my son and then watched Rayburn choke him. The restraint hold was originally authorized to use on autistic kids who would hit themselves. My son is not in special ed. They have eroded the initial acceptance of the restraint hold into a license. The nazis used COVID as an excuse to abuse my son, and assault me. It&#8217;s a mental sickness these people have. They will see me again in court.&#8221;</p>
<p><a href="https://www.givesendgo.com/unmaskdenverchildren" target="_blank" rel="noopener"><strong>Help support Anthony and Chase Chavez’s legal battle against Susan Rayburn and Lowry Elementary School here. </strong></a></p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/watch-special-ed-teacher-choked-7-year-old-refusing-wear-mask/">WATCH: Special Ed Teacher Choked 7-Year-Old For Refusing To Wear Mask</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></content:encoded>
					
		
		
		<enclosure url="http://www.thegatewaypundit.com/wp-content/uploads/chase-choked-.jpg" length="72799" type="image/jpeg" />	</item>
		<item>
		<title>&#8220;Decision to Abort a Child&#8221; &#8211; Biden&#8217;s Handlers Whisk Him Away After He Admits Abortion is Murder in Off-Script Remarks (VIDEO)</title>
		<link>https://www.thegatewaypundit.com/2022/05/decision-abort-child-bidens-handlers-whisk-away-admits-abortion-murder-off-script-remarks-video/</link>
		
		<dc:creator><![CDATA[Cristina Laila]]></dc:creator>
		<pubDate>Tue, 03 May 2022 16:54:00 +0000</pubDate>
				<category><![CDATA[Uncategorized]]></category>
		<guid isPermaLink="false">https://www.thegatewaypundit.com/?p=729556</guid>

					<description><![CDATA[<p>Joe Biden on Tuesday admitted abortion is murder in off-script remarks to reporters. Biden spoke to reporters on the tarmac at Joint Base Andrews Tuesday morning as he was preparing to depart to Alabama to visit a Lockheed Martin facility. Reporters peppered Biden with questions about the Supreme Court&#8217;s leaked draft opinion revealing the highest&#8230;</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/decision-abort-child-bidens-handlers-whisk-away-admits-abortion-murder-off-script-remarks-video/">&#8220;Decision to Abort a Child&#8221; &#8211; Biden&#8217;s Handlers Whisk Him Away After He Admits Abortion is Murder in Off-Script Remarks (VIDEO)</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></description>
										<content:encoded><![CDATA[<p><img loading="lazy" class="alignnone size-full wp-image-729559" data-src="https://www.thegatewaypundit.com/wp-content/uploads/IMG_2894.jpg" alt="" width="1169" height="628" /></p>
<p>Joe Biden on Tuesday admitted abortion is murder in off-script remarks to reporters.</p>
<p>Biden spoke to reporters on the tarmac at Joint Base Andrews Tuesday morning as he was preparing to depart to Alabama to visit a Lockheed Martin facility.</p>
<p>Reporters peppered Biden with questions about the<a href="https://www.thegatewaypundit.com/2022/05/breaking-supreme-court-vote-end-roe-v-wade-draft-opinion-justice-samuel-alito/" target="_blank" rel="noopener"> Supreme Court&#8217;s leaked draft opinion</a> revealing the highest court of the land is set to strike down Roe v Wade.</p>
<p>Biden was a bumbling mess and was unable to make a cogent point.</p>
<p>However, in a major flub, Biden accidentally admitted abortion is murder.</p>
<p>&#8220;The idea that we&#8217;re gonna make a judgment that is going to say that no one can make the judgment to choose to <strong>abort a child</strong> based on a decision by the Supreme Court I think goes way overboard,&#8221; said Biden as his handlers whisked him away.</p>
<p>&#8220;Come on guys! Let&#8217;s go!&#8221; Biden&#8217;s handler shouted to reporters as Biden walked away.</p>
<p>There goes the left&#8217;s &#8220;clump of cells&#8221; argument.</p>
<p>VIDEO:</p>
<p><iframe loading="lazy" title="Biden: Leaked Supreme Court Draft Opinion On Roe v. Wade &#039;Concerns Me A Great Deal&#039;" width="500" height="281" data-src="https://www.youtube.com/embed/nc6JNK9sUb8?start=225&#038;feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/decision-abort-child-bidens-handlers-whisk-away-admits-abortion-murder-off-script-remarks-video/">&#8220;Decision to Abort a Child&#8221; &#8211; Biden&#8217;s Handlers Whisk Him Away After He Admits Abortion is Murder in Off-Script Remarks (VIDEO)</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></content:encoded>
					
		
		
		<enclosure url="http://www.thegatewaypundit.com/wp-content/uploads/IMG_2894.jpg" length="81574" type="image/jpeg" />	</item>
		<item>
		<title>Biden Releases Statement on Supreme Court&#8217;s Decision Draft to End Roe v Wade &#8211; Doesn&#8217;t Mention Unprecedented Leak to Press</title>
		<link>https://www.thegatewaypundit.com/2022/05/biden-releases-statement-supreme-courts-decision-draft-end-roe-v-wade-doesnt-mention-unprecedented-leak-press/</link>
		
		<dc:creator><![CDATA[Cristina Laila]]></dc:creator>
		<pubDate>Tue, 03 May 2022 16:06:00 +0000</pubDate>
				<category><![CDATA[Uncategorized]]></category>
		<guid isPermaLink="false">https://www.thegatewaypundit.com/?p=729536</guid>

					<description><![CDATA[<p>Joe Biden Tuesday morning released a statement in response to a leaked draft opinion revealing the Supreme Court is set to strike down Roe v Wade. Via Politico: “The Supreme Court has voted to strike down the landmark Roe v. Wade decision, according to an initial draft majority opinion written by Justice Samuel Alito circulated inside&#8230;</p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/biden-releases-statement-supreme-courts-decision-draft-end-roe-v-wade-doesnt-mention-unprecedented-leak-press/">Biden Releases Statement on Supreme Court&#8217;s Decision Draft to End Roe v Wade &#8211; Doesn&#8217;t Mention Unprecedented Leak to Press</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></description>
										<content:encoded><![CDATA[<p><img loading="lazy" class="alignnone size-full wp-image-696603" src="https://www.thegatewaypundit.com/wp-content/uploads/51AA5BBF-1362-4C66-A603-83A4AE744E08-scaled.jpeg" alt="" width="2560" height="1440" srcset="https://www.thegatewaypundit.com/wp-content/uploads/51AA5BBF-1362-4C66-A603-83A4AE744E08-scaled.jpeg 2560w, https://www.thegatewaypundit.com/wp-content/uploads/51AA5BBF-1362-4C66-A603-83A4AE744E08-105x59.jpeg 105w" sizes="(max-width: 2560px) 100vw, 2560px" /></p>
<p>Joe Biden Tuesday morning released a statement in response to a leaked draft opinion revealing the Supreme Court is set to strike down Roe v Wade.</p>
<p>Via <a href="https://www.politico.com/news/2022/05/02/supreme-court-abortion-draft-opinion-00029473" target="_blank" rel="noopener">Politico</a>: “The Supreme Court has voted to strike down the landmark Roe v. Wade decision, according to an initial draft majority opinion written by Justice Samuel Alito circulated inside the court and obtained by POLITICO.”</p>
<p>Justice Alito’s opinion is a “full-throated, unflinching repudiation” according to Politico.</p>
<p>“Roe was egregiously wrong from the start,” Alito wrote. “We hold that Roe and Casey must be overruled. It is time to heed the Constitution and return the issue of abortion to the people’s elected representatives.”</p>
<p>The draft opinion was leaked to the press – something that is unprecedented. Of course, most assume the leaker is a liberal clerk who hopes to change the outcome of the case.</p>
<p>Chief Justice of the Supreme Court John Roberts released a statement on the unprecedented leak. <a href="https://www.thegatewaypundit.com/2022/05/breaking-supreme-court-chief-justice-releases-statement-unprecedented-scotus-leak-confirms-authenticity-calls-investigation/" target="_blank" rel="noopener">Roberts reportedly confirmed its authenticity</a> and called for an investigation.</p>
<p>Joe Biden did not mention the leak in his statement &#8211; of course he didn&#8217;t.</p>
<p>Biden did however use the unprecedented leak to call on Congress to codify Roe into law.</p>
<p>Biden also used the leak to campaign for the midterms: &#8220;At the federal level, we will need more pro-choice Senators and a pro-choice majority in the House to adopt legislation that codifies Roe, which I will work to pass and sign into law,&#8221; Biden said.</p>
<p><img loading="lazy" class="alignnone size-full wp-image-729539" data-src="https://www.thegatewaypundit.com/wp-content/uploads/FR1ncFMXoAAuSN8-scaled.jpg" alt="" width="1812" height="2560" /></p>
<p>The post <a rel="nofollow" href="https://www.thegatewaypundit.com/2022/05/biden-releases-statement-supreme-courts-decision-draft-end-roe-v-wade-doesnt-mention-unprecedented-leak-press/">Biden Releases Statement on Supreme Court&#8217;s Decision Draft to End Roe v Wade &#8211; Doesn&#8217;t Mention Unprecedented Leak to Press</a> appeared first on <a rel="nofollow" href="https://www.thegatewaypundit.com">The Gateway Pundit</a>.</p>
]]></content:encoded>
					
		
		
		<enclosure url="http://www.thegatewaypundit.com/wp-content/uploads/51AA5BBF-1362-4C66-A603-83A4AE744E08-scaled.jpeg" length="263970" type="image/jpeg" />	</item>
	</channel>
</rss>
'''

if __name__ == "__main__":
    soup = BeautifulSoup(test, 'xml')
    parsed = parse_soup(soup)
    print(parsed[0])
   #save_xml_date(datetime?) 
   # date input from airflow?