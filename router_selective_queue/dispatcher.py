def balance_dispatch(web_queue, cbr_queue, ep, sp, val):
    # web packet sent only when delay is 2 times or more bigger
    if web_queue[0].delay(ep.time_actual) > 2 * cbr_queue[0].delay(ep.time_actual):
        packet_dispatch(web_queue, ep, sp, val)
    else:
        packet_dispatch(cbr_queue, ep, sp, val)


def packet_dispatch(queue, ep, sp, val):
    # packet dispatch process
    packet = queue.pop(0)
    ep.time_packet_exit = ep.time_actual + (packet.size / sp.link_size)
    ep.router_working = True

    # update utilization
    val.use(ep.time_actual, ep.time_packet_exit)
    val.enter(ep.time_actual)
