�
��kXc           @   s`  d  Z  d d l Z d d l Z d d l m Z d d l m Z d d l m Z d d l m	 Z	 d d l
 m Z m Z d d l
 m Z d d	 l m Z d d
 l m Z d d l m Z d d l m Z d d l m Z d d l m Z d d l m Z m Z d d l m Z d d l m Z m Z d d l Z  d d l! Z! d d l" Z# e! j$ j% d d � d k rtd GHe# j& d � n  d d l' j( Z) d d
 l m Z d d l* Z* d d l+ Z+ d d l! Z! e! j, j- e! j, j. e! j, j/ e0 � d � � Z, e, e+ j, k r
e+ j, j1 d e, � n  [, d d l2 m2 Z2 d d l3 m4 Z4 d e5 f d �  �  YZ6 d e j7 f d �  �  YZ8 d S(   s�  
Controller_Core - a ryu application for the team 4 project
The code uses the topology discovery code sourced from [1] as a starting point. The original code is based on Openflow v1 and uses ryu topology api
and flooding to build the topology. However, it underwent major modification to support below features:

-topology discovery without ARP flooding the network. To bootstrap the network, one must perform  pingall in the mininet.
-Implement a discrete graph from the data provided by topology api
-Compute shortest path from the graph
-Install flows in the all the switches in a path to route a packet from one node to another

References:
    [1] https://sdn-lab.com/2014/12/31/topology-discovery-with-ryu/
i����N(   t   pprint(   t   app_manager(   t   deque(   t	   ofp_event(   t   MAIN_DISPATCHERt   CONFIG_DISPATCHER(   t
   set_ev_cls(   t   ofproto_v1_3(   t   haddr_to_bin(   t   packet(   t   ethernet(   t   arp(   t   ether_types(   t
   get_switcht   get_link(   t   ControllerBase(   t   eventt   switchest   DISPLAYt    s3   no display found. Using non-interactive Agg backendt   Aggs   ../libi   (   t   datetime(   t   client_sidet   SharedContextc           B   s   e  Z d  �  Z RS(   c         C   s%   t  j �  |  _ t |  _ d |  _ d  S(   Ni    (   t   nxt   DiGrapht   learnt_topologyt   Falset   bootstrap_completet   time_of_last_fetch(   t   self(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __init__A   s    	(   t   __name__t
   __module__R   (    (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR   @   s   t   ProjectControllerc           B   s2  e  Z d  Z i e d 6Z e j g Z d �  Z d �  Z	 e
 e j e � d �  � Z d �  Z d �  Z d �  Z d �  Z d	 �  Z d
 �  Z d �  Z d �  Z e
 e j e � d �  � Z d �  Z d �  Z e
 e j � d �  � Z d �  Z d �  Z  d �  Z! d �  Z" d �  Z# d �  Z$ d �  Z% d �  Z& d �  Z' RS(   s    CPM module for CSD Team4 projectt   networkc         O   sa  t  t |  � j | | �  t |  _ | d |  _ |  j j |  _ |  j j	 d |  j j
 � i t d 6t d 6t d 6|  _ t |  _ i d d 6t d 6t d	 6d
 d 6d d 6d d 6d d 6|  _ |  j d |  _ t |  j � |  _ t j d t � |  _ |  j j t j � t j |  j d � } | j t j � t j d � } | j | � |  j j | � |  j j	 d |  j j �  � i  |  _ t j d d d d d g � |  _  i  |  _! i  |  _" |  |  _# i  |  _$ i  |  _% d |  _& d |  _' d |  _( i  |  _) |  j j	 d � t* t+ j+ �  � |  _, d |  _- d |  _. d |  _/ i  |  _0 t1 �  |  _2 |  j j	 d |  j- |  j/ � d  S(   NR#   sH   SHARED_CONTEXT : SharedContext Instantiated and time_of_last_fetech = %rt   RPMt   HUMt   NFMs   ff:ff:ff:ff:ff:fft	   bcast_mact   bootstrap_in_progresst"   flow_table_strategy_semi_proactives   /var/www/html/spaceyt   logdirs#   /var/www/html/spacey/cpmweights.logt	   cpmlogdirs   http://127.0.0.1:8000/Tasks.txtt   metrics_fetch_rest_urli   t   fetch_timer_in_secondst   cpms)   %(asctime)s - %(levelname)s - %(message)ss#   Starting up cpmlogger. edges are %rt	   core_utilt	   mem_usaget
   rpm_weightt	   link_utilt   sw_packet_drop_ratei    s&   controller_core module starting up....i   iF   s&   BOOTSTRAP, type = %r , host_count = %r(3   t   superR"   R   t   Truet"   disable_cpm_openflow_ruleinstallert   shared_contextR   t   nett   loggert   infoR   R   t   modules_enabledt   install_openflow_rulest	   defines_Dt   rest_urlR   t   DMclientt   loggingt	   getLoggerR    t	   cpmloggert   setLevelt   DEBUGt   FileHandlert	   Formattert   setFormattert
   addHandlert   edgest   l2_dpid_tablet   dictt   fromkeyst   edge_weightst   l2_ip2mac_tablet   l2_mac2ip_tablet   topology_api_appt   nodest   linkst   no_of_nodest   no_of_linkst   it   rxpkts_types_Dt   intt   timet   epoc_starttimet   network_bootstrap_typet   network_bootstrap_timet!   network_bootstrap_discovery_countt
   datapathDbt   sett   already_installed_paths_SET(   R   t   argst   kwargst   handlert	   formatter(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR   d   sX    		
	!													c         C   s;   d j  g  t | � D] } | d d k r | ^ q � GHd  S(   Ns   
i    t   _(   t   joint   dir(   R   t   objt   x(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   ls�   s    c         C   s_   | j  j } | j } | j } | j �  } | j | j | j � g } |  j | d | | � d S(   s�   
        Openflow v1.3 requires that table-miss flow entry rule be installed by the controller to direct the packets to the controller that do not match
        existing rule.
        i    N(	   t   msgt   datapatht   ofprotot   ofproto_parsert   OFPMatcht   OFPActionOutputt   OFPP_CONTROLLERt   OFPCML_NO_BUFFERt   add_flow(   R   t   evRk   Rl   t   parsert   matcht   actions(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   switch_features_handler�   s    		c   	   	   C   s_   | j  } | j } | j | j | � g } | j d | d | d | d | � } | j | � d S(   sy   
            add_flow for openflow v1.3
            Note that it installs an instruction from the actions input.
        Rk   t   priorityRu   t   instructionsN(   Rl   Rm   t   OFPInstructionActionst   OFPIT_APPLY_ACTIONSt
   OFPFlowModt   send_msg(	   R   Rk   Rx   Ru   Rv   Rl   Rt   t   instt   mod(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyRr   �   s    		c         C   s"   t  j |  j | | d t �} | S(   Nt   weighted(   R   t   shortest_pathR8   R5   (   R   t   src_nodet   dst_nodet   sp_L(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR�     s    c         C   s  |  j  d r� |  j d k rg t t j �  � |  j |  j k rg t |  j  d <|  j j d |  j � qg n  |  j d k r� t	 |  j
 � |  j k r� t |  j  d <|  j j d |  j � q� q� n  |  j  d |  _ |  j  d |  j _ |  j r� |  j j d � n |  j j d � d S(   sR   has the criteria for bootstrap completion met, if yes then set the completion flagR(   i    s    Bootstrap type %d just Completedi   s   CPM: BOOTSTRAP TO NFM COMPLETEs'   CPM: BOOTSTRAP NFM xxxxxxx NOT COMPLETEN(   R=   RZ   RW   RX   RY   R[   R   R9   t   debugt   lenRO   R\   R   R7   RB   R:   (   R   (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __check_bootstrap_completion  s    "	c         C   s7   t  | � } | j �  } | j �  } | | t | � f S(   s�  
        :param spath:
        this function is not tested yet
        returns a list after having removed first and last element from spath which are src_mac and dst_mac respectively
        this must be done in the most efficent manner python has to offer so we use deque,  see timeit benchmarks at below URL
        URL  : http://stackoverflow.com/questions/33626623/the-most-efficient-way-to-remove-first-n-elements-in-a-python-list
        :return:
        (   R   t   popt   popleftt   list(   R   t   spatht   spath_dqt   dst_mact   src_mac(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt    __remove_macs_from_shortest_path'  s    
c         C   s  |  j  j d | � t | � } d } | | d } | | d } x� | | d k r|  j  j d | � | | } | | d } | | d } |  j j | | d }	 |  j  j d | | |	 � |  j j | | d }
 |  j  j d | | |
 � |  j | | |	 | |
 � | d } qD W| d	 } | | d } | d } x� | d k r|  j  j d
 | � | | } | | d } | | d } |  j j | | d }	 |  j  j d | | |	 � |  j j | | d }
 |  j  j d | | |
 � |  j | | |	 | |
 � | d } q;Wd S(   s  
        input is a networkx shortest path list of the format [src_mac, switch1, sw2,..., swN, dst_mac]
        it installs flows in all the switches1..N
        :rtype: Boolean
        :param spath
        :return: true if operation was successful or else false
        s   Considering path %ri   i   s    Installing rule : iteration = %rt   dst_portsB   FWD FLOW in_port computed = self.net.edge[%r][%r]['dst_port'] = %rt   src_portsD   FWD FLOW out_port computed = self.net.edge[%r][%r]['src_port'] = %r i    s"   Installing rule : iteration = %r  sJ   REV FLOW in_port computed = self.net.edge[%r][%r]['dst_port/in_port'] = %rsK   REV LOW out_port computed = self.net.edge[%r][%r]['src_port/out_port'] = %rN(   R9   R�   R�   R8   t   edget!   _ProjectController__send_flow_mod(   R   t   spath_with_macst   nRU   R�   R�   t   sw_bt   sw_ct   sw_at   in_portt   out_port(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __install_path_flow6  s>    




c         C   s  |  j  j d | | | | | � |  j | } | j } | j } d }	 }
 d } d } } d } | j } | j d | d | d | � } | j | � g } | j | j	 | � g } | j
 | |	 |
 | | j | | | | | j | j | j | | � } | j | � d  S(   NsC   FLOWMOD_1 : installing rule: %r -----> %r ==== %r === %r -----> %r i    i �  R�   t   eth_dstt   eth_src(   R9   R�   R]   Rl   Rm   t   OFP_NO_BUFFERRn   Ro   Rz   R{   R|   t	   OFPFC_ADDt   OFPP_ANYt   OFPG_ANYt   OFPFF_SEND_FLOW_REMR}   (   R   t   dpidR�   R�   R�   R�   Rk   t   ofpt
   ofp_parsert   cookiet   cookie_maskt   table_idt   idle_timeoutt   hard_timeoutRx   t	   buffer_idRu   Rv   R~   t   req(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __send_flow_mod�  s*    		

		c         C   s   | |  j  | j <d  S(   N(   R]   t   id(   R   Rk   (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __save_datapath�  s    c         C   s]   t  | � } | |  j k r2 |  j j d | � t S|  j j | � |  j j d | � t Sd  S(   Ns%   ___PATH_ALREADY_INSTALLED____ i.e. %rs)   ---PATH_NOT_ALREADY_INSTALLED---- i.e. %r(   t   tupleR_   R9   R�   R5   t   addR   (   R   R�   t   spath_as_tuple(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __isPathNotAlreadyInstalled�  s    c         C   s)  |  j  �  |  j �  |  j �  | j } | j } |  j | � | j } | j d } | r\ n |  j j	 d � t
 j | j � } | j t j � } | j } | j }	 | j }
 | j t j k r� d  S| |  j d k r�|  j j d |	 |
 | j d � | j t j � } | sd  S|	 |  j k ra|  j j d |	 � i i | j d d 6| j d 6|	 6|  j |
 <|	 |  j | j <| j |  j |	 <|  j j d | j | j | j � |  j j |	 |
 i | j d d 6| j d d	 6|	 d
 6|
 d 6t  d 6| j d 6d d 6d d 6� |  j j |
 |	 i | j d d 6| j d d	 6|
 d
 6|	 d 6t  d 6d d 6d d 6� |  j  �  q%| j t j! k r�|  j j d � d  S|  j j d � | j |  j k r�|  j j d � d  S|  j | j } |  j | } |  j j d | | j � t
 j �  } | j" t j d | j d | j d | � � | j" t j d t j# d | d | d |	 d | j � � |  j j d � |  j$ | | | � |  j j d � n�|  j d r�|  j j% d  � d  S|  j j d! � |  j j d" � | |  j k r|  j& r�d  S|  j j d# | � |  j j d$ | |	 � t' j( |  j |	 | � sO|  j j d% |	 | � d  S|  j) �  |  j j% d& � |  j* j d' |  j j+ �  � |  j, �  |  j j% d( � t' j- |  j |	 | � } |  j j d) |	 | | � |  j. | � r|  j j d* | � |  j/ | � qn |  j j d+ | |	 � |  j, �  d  S(,   NR�   s"   EMPTY in_port in Packet-IN messageR'   sG   broadcast received from src mac = %s , switch dpid = %r at in_port = %rs:   LEARNING : learning a new src_mac = %r for the first time t   ips�   LEARNING : ARP extractions show about packet details as : arp.src_ip = %r , arp.dst_ip = %r , arp.opcode (1 for Request)  = %r  R�   R�   t   src_dpidt   dst_dpidt   end_hosti
   t   bwi   t   weights)   IGNORING packet as its not an arp requests�   RX_BCAST_SRC_MAC_ALREADY_LEARNT: Received a broadcast packet with source mac alrd in our l2_table, creating arp reply and attaching to OF packet_outs^   RX_BCAST..:Src Mac known but havent learnt the target IP yet i.e. arp.dst_ip's mac yet. ReturnsF   KEY1 : Found dst_mac %r for arp header dst ip %r , puttin in arp replyt	   ethertypet   dstt   srct   opcodeR�   t   src_ipR�   t   dst_ips   Crafting an ARP replys   Sending arp reply reply doneR(   s~   RX_NO_BCddAST_ONLY_TARGETED_DST_MAC : Sorry network bootstrap still in progress not computing spath , not installing any flowst6   ______________________________________________________s|   __________RX_NO_BCAST_ONLY_TARGETED_DST_MAC : Network Bootstrap Completed. Proceeding with shortest path calculation________sn   RX_NO_BCAST_ONLY_TARGETED_DST_MAC: ALREADY_LEARNT: Received ARP to specific dst mac %r that exist in our graphs>   Do we have a path to this destination mac? src= %r , dst = %r sP   Cannot find path from src mac %r to dst_mac %r, returning ie. doing nothing mores1   ________________ WEIGHTED_TOPOLOGY begin ________s   WEIGHTED_TOPOLOGY: = %rs.   ________________ WEIGHTED_TOPOLOGY end________s7   Found shortest path from src mac %r to dst mac %r as %rs   Installing path : %rs$   LEARN_NEW_MAC dst_mac=%r src_mac=%r (0   t   print_l2_tablet.   _ProjectController__check_bootstrap_completiont   save_topolog_to_fileRj   Rk   t!   _ProjectController__save_datapathRl   Ru   R9   t   errorR	   t   Packett   datat   get_protocolR
   R�   R�   R�   R�   R   t   ETH_TYPE_LLDPR=   R�   R   R8   R�   RJ   RN   RO   R�   R�   t   add_edgeR5   t   ARP_REQUESTt   add_protocolt	   ARP_REPLYt   _send_packetR:   R6   R   t   has_pathtI   _ProjectController__fetch_ALL_metrics_and_insert_weight_in_topology_graphRB   RI   t   show_graph_statsR�   t-   _ProjectController__isPathNotAlreadyInstalledt%   _ProjectController__install_path_flow(   R   Rs   Rj   Rk   Rl   R�   t   pktt   pkt_ethR�   R�   R�   t   pkt_arpt   mac_of_arp_dst_ipt   ip_of_arp_dst_mact   new_pktR�   (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   _packet_in_handler�  s�    


						 ,"'		
		

 ?c         C   s�   t  j |  j � } t  j |  j | d t d t �t  j |  j d � } t  j |  j | d | �|  j d d } t	 j
 | � t  j |  j d � } t  j |  j | d | �|  j d d } t	 j
 | � t	 j �  d  S(	   Nt   with_labelst   holdR�   t   edge_labelsR*   s   /CPM_network_with_src_port.pngR�   s   /CPM_network_with_dst_port.png(   R   t   spring_layoutR8   t   drawR5   R   t   get_edge_attributest   draw_networkx_edge_labelsR=   t   pltt   savefigt   clf(   R   t   post	   label_srct   filename_srct	   label_dstt   filename_dst(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR�   �  s    c         C   s|   |  j  d rh |  j j d |  j j �  � |  j j d |  j j �  � |  j j d |  j � |  j �  n |  j j d � d  S(   NR(   s!   list of edges: self.net.edges %s s   list of nodes: 
 %rs   l2_lookup_table : %rtD   _________________________bootstrap__completed_______________________(   R=   R9   R�   R8   RI   RQ   RJ   R�   (   R   (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR�     s    c         C   sE  |  j  j d | � t |  j d  � } t |  j d  � } g  | D]c } | j j | j j i | j j	 d 6| j j	 d 6| j j
 d 6| j j
 d 6d d 6d d	 6f ^ q> } g  | D]c } | j j | j j i | j j	 d 6| j j	 d 6| j j
 d 6| j j
 d 6d d 6d d
 6f ^ q� } |  j j | � |  j j | � |  j �  d  S(   Ns   EventSwitchEnter observed: %rR�   R�   t   dst_namet   src_namei
   R�   i   t   wegihtR�   (   R9   R�   R   RP   t   NoneR   R�   R�   R�   t   port_not   nameR8   t   add_edges_fromR�   (   R   Rs   t   switch_listt
   links_listt   linkt   links_onedirection_Lt   links_opp_direction_L(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   get_topology_data  s    'mm!c         C   sF   |  j  j d |  j � |  j  j d |  j � |  j  j d |  j � d  S(   Ns   l2_table = %rs   l2_mac2ip = %rs   l2_ip2mac = %r(   R9   R�   RJ   RO   RN   (   R   (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR�   �  s    c         C   s�   |  j  j d � | j } | j } | j �  |  j  j d | f � | j d | � g } | j d | d | j d | j	 d | d | j
 � } | j | � d  S(	   Ns$   Sending an arp reply in _send_packets   crafted arp reply packet-out %st   portRk   R�   R�   Rv   R�   (   R9   R�   Rl   Rm   t	   serializeR:   Ro   t   OFPPacketOutR�   Rp   R�   R}   (   R   Rk   R�   R�   Rl   Rt   Rv   t   out(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR�   �  s    		
		c         C   s   t  | t | | � � S(   N(   t   maxt   min(   R   R�   t   smallestt   largest(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   clamp�  s    c         C   s�   |  j  j d | � yG | |  j j | | | <|  j  j d | | |  j j | | d � Wni t k
 r} |  j  j d � nI t k
 r� |  j  j d � n) t k
 r� } |  j  j d d t	 �n Xd S(	   sA   key can be <module_name><module_key> e.g. 'nfm_link_utilization' s$   FETCH UPDATE_GRAPH_NFM , weight = %rs9   FETCH Assigned value self.net.edge[%r][%r]['weight'] = %rs   weight]s"   FETCH KeyError when updating graphs#   FETCH NameError when updating graphs=   Unable to update this key in the graph, here is the tracebackt   exc_infoN(
   R9   R:   R8   R�   R�   t   KeyErrorR�   t	   NameErrort	   ExceptionR5   (   R   R�   R�   t   keyt   valuet   e(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __update_graph�  s    /c         C   s�  t  t t j �  d � � |  _ |  j d d } |  j j d | � |  j |  j j | k rn |  j d rn d S|  j |  j _ |  j	 j d |  j j � d } d } d } |  j d r� |  j �  } n  |  j d r� |  j �  } n  |  j d	 r� |  j �  } n  x� |  j j d
 t � D]� \ } } } t | � d t | � } t | � d t | � }	 y d | k rjwn  Wn? t k
 r�}
 |  j j d |
 � |  j j d | d t �n X|  j t | � t | � | | | � } |  j | | d | � qWd S(   sh  
        Iterate over the topology graph and from each of the supported modules: NFM, RPM, HUM, do following:
        -fetch the module metrics for each link
        -compute weight of the link based on all the fetched metrics (see the Teacher's approved metrics document)
        -add this computed weight to the link in the topology
        :return:
        i�  R-   sT   FETCH_ALL_METRICS : fetch_metric_and_insert, time_max_limit = fetch every %r secondsR(   NsJ   FETCH_ALL_METRICS : About to fetch remote metrics, time_of_last_fetch = %rR&   R$   R%   R�   t   -t   :s:   Exception encountered when parsing a graph node =%r for : R  R�   (   RW   t   roundRX   t   current_timeR=   R9   R�   R7   R   RB   R�   R;   t(   _ProjectController__REST_get_NFM_metricst(   _ProjectController__REST_get_RPM_metricst(   _ProjectController__REST_get_HUM_metricsR8   t
   edges_iterR5   t   strR  R�   t'   _ProjectController__compute_link_weightt   unicodet    _ProjectController__update_graph(   R   t   time_max_limitt   nfm_metrics_datat   rpm_metrics_datat   hum_metrics_dataR�   R�   R�   t   src_to_dst_nodet   dst_to_src_nodeR  t   link_weight(    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt7   __fetch_ALL_metrics_and_insert_weight_in_topology_graph�  s<     
%

'c         C   s?  d } d } d } |  j  d r� | r� d }	 d }
 | d d } | d d } |	 t | t | � d t | � � |
 t | t | � d t | � � } d | } n  |  j  d r� | r� d } n  |  j  d r-| r-d	 } d
 } | d d } | d d } | t | j � | t | � } d | } n  | | | } | S(   s�  
        returns the link weight value computed according to the Metrics description document from the metrics data retrieved from different modules
        :param src_node: src dpid of the link , must be in unicode
        :param dst_node: dst dpid of the link, must be in unicode
        :param nfm: nfm metrics data , it will be already set to False if NFM REST get read a blank payload or GET connection failed.
        :param rpm: --do--
        :param hum:  --do--
        :return:
        i    R&   g      �?i   R	  g��Q��?R$   R%   g�������?g�������?gZd;�O�?(   R;   t   floatR  t   sumt
   itervalues(   R   R�   R�   t   nfmt   rpmt   humt   nfm_total_weightt   rpm_total_weightt   hum_total_weightt   nfm_link_util_weightt   nfm_packet_dropped_weightt   nfm_link_utilt   nfm_packet_droppedt   hum_core_weightt   hum_memory_weightt	   hum_corest
   hum_memoryR  (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __compute_link_weight%  s,    
%)	!c         C   s�   t  } i d d 6d d g d 6} y |  j j | � } WnC t k
 r{ } |  j j d | � |  j j d d t  �t } d  SX|  j j d	 | � | d
 d o� | d d s� |  j j d � |  j j d | � t } n  |  j j d | � | S(   NR   t   modulet   link_utilizationt   packet_droppedt   keylists5   FETCH_NFM_METRICS : HTTP Failure ...., Exception = %rs6   FETCH_NFM_METRICS : HTTP Failure ...., Exception traceR  s9   FETCH_NFM_METRICS: -----> EMPTY - nfm_metrics_data  = %r i    i   s�   FETCH_NFM_METRICS : Empty NFM data read, key value, either or both of link_util or packet_drop is empty. DM,DB running but blank data served.s)   FETCH_NFM_METRICS : nfm_metrics_data = %rs<   FETCH_NFM_METRICS: HTTP GET RESULT - nfm_metrics_data  = %r (   R5   R?   t   getmeR  RB   R�   R   R�   (   R   R  t   nfm_what_metrics_to_fetchR  (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __REST_get_NFM_metricsQ  s     	c         C   s�   t  } i d d 6d d g d 6} y |  j j | � } WnC t k
 r{ } |  j j d | � |  j j d d t  �t } d	 SX| d
 d r� | d d r� |  j j d � t } n |  j j d | � | S(   s�   
        In response to HTTP GET request, the sample response hum_metrics_data is :
        h = [[u'core', {u'0': 11.11, u'1': 13.11,}]  , [u'memory', 89]]
        core dict is h[0][1]
        memory util is h[1][1]
        R"  R/  t   coret   memoryR2  s5   FETCH_HUM_METRICS : HTTP Failure ...., Exception = %rs6   FETCH_HUM_METRICS : HTTP Failure ...., Exception traceR  Ni    i   s�   FETCH_HUM_METRICS : Empty HUM data read, key value, either or both of link_util or packet_drop is empty. DM,DB running but blank data serveds/   FETCH_HUM_METRICS: OK - hum_metrics_data  = %r (   R5   R?   R3  R  RB   R�   R   R�   (   R   R  t   hum_what_metrics_to_fetchR  (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __REST_get_HUM_metricsh  s    	c      	   C   s�   t  } i d d 6d d d d d d d	 d
 g d 6} y |  j j | � } WnC t k
 r� } |  j j d | � |  j j d d t  �t } d  SX| d d s� | d d r� |  j j d � t } n  |  j j d | � | S(   NR!  R/  t   delayst   normalized_delayst   max_latencyt   min_latencyt   mean_latencyt   median_latencyt   25th_latencyt   75th_latencyR2  s/   FETCH_RPM_METRICS : Failed ...., Exception = %rs0   FETCH_RPM_METRICS : Failed ...., Exception traceR  i    i   s�   FETCH_RPM_METRICS : Empty RPM data read, key value, either or both of link_util or packet_drop is empty. DM,DB running but blank data serveds/   FETCH_RPM_METRICS: OK - hum_metrics_data  = %r (   R5   R?   R3  R  RB   R�   R   R�   (   R   R  t   rpm_what_metrics_to_fetchR  (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   __REST_get_RPM_metrics�  s     		((   R    R!   t   __doc__R   t	   _CONTEXTSR   t   OFP_VERSIONt   OFP_VERSIONSR   Ri   R   R   t   EventOFPSwitchFeaturesR   Rw   Rr   R�   R�   t2   _ProjectController__remove_macs_from_shortest_pathR�   R�   R�   R�   t   EventOFPPacketInR   R�   R�   R�   R   t   EventSwitchEnterR�   R�   R�   R   R  R�   R  R  R  R  (    (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyR"   H   s8   	j						Z			� 	,	�					g	,		(9   RD  R@   t   structR    t   ryu.baseR   t   collectionsR   t   ryu.controllerR   t   ryu.controller.handlerR   R   R   t   ryu.ofprotoR   t   ryu.lib.macR   t   ryu.lib.packetR	   R
   R   R   t   ryu.topology.apiR   R   t   ryu.app.wsgiR   t   ryu.topologyR   R   t   networkxR   t   ost
   matplotlibt   mplt   environt   gett   uset   matplotlib.pyplott   pyplotR�   RX   t   syst   patht   abspathRe   t   dirnamet   __file__t   insertR   t   clientR   t   objectR   t   RyuAppR"   (    (    (    sD   /sdn_monitoring_branches/controller_core/src/controller_core_of13.pyt   <module>   sR   -� � � � �