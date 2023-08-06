from cohesivenet import util, Logger


def create_firewall_policy(client, firewall_rules, state={}):
    """Create group of firewall rules

    Arguments:
        client {VNS3Client}
        firewall_rules {List[CreateFirewallRuleRequest]} - [{
            'position': int,
            'rule': str
        }, ...]

    Keyword Arguments:
        state {dict} - State to format rules with. (can call client.controller_state)

    Returns:
        Tuple[List[str], List[str]] - success, errors
    """
    successes = []
    errors = []
    Logger.debug(
        "Creating firewall policy.",
        host=client.host_uri,
        rule_count=len(firewall_rules),
    )
    for i, rule_args in enumerate(firewall_rules):
        rule = rule_args["rule"]
        if util.is_formattable_string(rule):
            try:
                rule = rule.format(**state)
                rule = rule.format(**state)
                rule_args.update(rule=rule)
            except KeyError as e:
                errors.append("Rule %d missing state args %s" % (i, ",".join(e.args)))
                continue

        client.firewall.post_create_firewall_rule(rule_args)
        successes.append(
            'Rule "%s" inserted at position %d' % (rule, rule_args["position"])
        )
    return successes, errors
