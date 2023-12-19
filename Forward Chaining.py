# Define a class for a rule
class Rule:
    def __init__(self, conditions, action):
        self.conditions = conditions
        self.action = action

    # Evaluate if all conditions are met
    def evaluate(self, facts):
        if all(condition in facts for condition in self.conditions):
            return self.action
        else:
            return None

# Define a class for a rule-based system
class RuleBasedSystem:
    def __init__(self):
        self.rules = []

    # Add a rule to the system
    def add_rule(self, conditions, action):
        self.rules.append(Rule(conditions, action))

    # Apply rules to a set of facts
    def apply_rules(self, facts):
        new_facts = set()
        actions_to_add = {}

        # Evaluate each rule
        for rule in self.rules:
            action = rule.evaluate(facts)
            if action is not None:
                if action in facts:
                    actions_to_add[action] = rule.action
                else:
                    new_facts.add(action)

        # Update facts with new actions
        new_facts.update(actions_to_add.values())
        return new_facts

# Function to get initial facts from the user
def get_initial_facts():
    facts_input = input("Enter initial facts (comma-separated): ")
    return set(facts_input.split(','))

# Function to get user-defined rules
# Condition = antecedent
# Action = consequent
def get_user_rules():
    print("Enter rules (condition and action) or 'q' to quit:")
    rules = []
    while True:
        condition = input("Condition (use 'and' to separate multiple conditions): ")
        if condition == 'q':
            break
        action = input("Action: ")
        rules.append((condition.split(' and '), action))
    return rules

# Excecuting The Functions
# Main Program

# Create the rule-based system
system = RuleBasedSystem()

# Get initial facts from user
facts = get_initial_facts()

# Get rules from user
rules = get_user_rules()
for conditions, action in rules:
    system.add_rule(conditions, action)

# Apply rules excluding initial facts
new_facts = system.apply_rules(facts)

# Include actions for conditions in new facts
for condition in new_facts.copy():
    action = system.apply_rules({condition})
    new_facts.update(action)

# Remove facts that already exist in the initial set
new_facts = new_facts.difference(facts)

# Filter facts that have both conditions in initial facts and new facts
new_facts = {fact for fact in new_facts if all(condition in facts.union(new_facts) for condition in fact.split(' and '))}

# Include actions for conditions in new facts again
for condition in new_facts.copy():
    action = system.apply_rules({condition})
    new_facts.update(action)

# Check if any new fact's conditions are met by the existing facts
for condition, action in rules:
    conditions_met = all(cond in facts.union(new_facts) for cond in condition)
    if conditions_met and action not in facts:
        new_facts.add(action)

# Print new facts
print("New Facts:", new_facts)
