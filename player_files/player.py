import tools.error_handling as error_handling

class Player:
    def __init__(self,
            name=None,

            level=1, exp=1, 
            player_class=None,

            cindrals=0,

            strength=1, 
            core_strength=1, core_strength_exp=0, current_cs_area=None,
            upper_body=1, upper_body_exp=0, current_ub_area=None,
            grip=1, grip_exp=0, current_grip_area=None,
            lower_body=1, lower_body_exp=0, current_lb_area=None,

            speed=1,
            reaction_time=1, reaction_time_exp=0, current_rt_area=None,
            velocity=1, velocity_exp=0, current_velo_area=None,
            acceleration=1, acceleration_exp=0, current_accel_area=None,
            agility=1, agility_exp=0, current_agil_area=None,

            durability=1,
            lung_capacity=1, lung_capacity_exp=0, current_lc_area=None,
            stamina=1, stamina_exp=0, current_stam_area=None,
            regeneration=1, regeneration_exp=0, current_regen_area=None,
            toughness=1, toughness_exp=0, current_tough_area=None,

            intelligence=1,
            STEM_knowledge=1, STEM_knowledge_exp=0,current_stem_area=None,
            logic=1, logic_exp = 0, current_logic_area=None,
            strategy=1, strategy_exp=0, current_strat_area=None,
            problem_solving=1, problem_solving_exp=0, current_ps_area=None,

            magic=1,
            mana_control=1, mana_control_exp=0,current_mc_area=None,
            spell_power=1, spell_power_exp=0, current_sp_area=None,
            magic_resistance=1, magic_resistance_exp=0, current_mr_area=None,

            swordsmanship=1, farming=1, fishing=1, mining=1, spells=None,

            inventory=[],
            weapon=None,
            helmet=None,
            chestplate=None,
            leggings=None,
            belt=None,
            left_glove=None,
            right_glove=None,
            boots=None,
            accessories=None,

            rebirths=0,
            reality_shards=0,
            training_bonus = 1


    ):
        
        self.name = name
        self.level = level
        self.exp = exp

        self.player_class = player_class
        self.cindrals = cindrals

        self.strength = strength
        self.core_strength_data = [core_strength, core_strength_exp, current_cs_area]
        self.upper_body_data = [upper_body, upper_body_exp, current_ub_area]
        self.grip_data = [grip, grip_exp, current_grip_area]
        self.lower_body_data = [lower_body, lower_body_exp, current_lb_area]

        self.speed = speed
        self.reaction_time_data = [reaction_time, reaction_time_exp, current_rt_area]
        self.velocity_data = [velocity, velocity_exp, current_velo_area]
        self.acceleraction_data = [acceleration, acceleration_exp, current_accel_area]
        self.agility_data = [agility, agility_exp, current_agil_area]

        self.durability = durability
        self.lungs_data = [lung_capacity, lung_capacity_exp, current_lc_area]
        self.stamina_data = [stamina, stamina_exp, current_stam_area]
        self.regeneration_data = [regeneration, regeneration_exp, current_regen_area]
        self.toughness_data = [toughness, toughness_exp, current_tough_area]

        self.intelligence = intelligence
        self.stem_data = [STEM_knowledge, STEM_knowledge_exp, current_stem_area]
        self.logic_data = [logic, logic_exp, current_logic_area]
        self.strategy = [strategy, strategy_exp, current_strat_area]
        self.problem_solving = [problem_solving, problem_solving_exp, current_ps_area]

        self.magic = magic
        self.mana_control_data = [mana_control, mana_control_exp, current_mc_area]
        self.spell_power_data = [spell_power, spell_power_exp, current_sp_area]
        self.magic_resistence_data = [magic_resistance, magic_resistance_exp, current_mr_area]

        self.swordsmanship = swordsmanship
        self.fishing = fishing
        self.mining = mining
        self.spells = spells

        self.inventory = inventory
        self.weapon = weapon
        self.helmet = helmet
        self.chestplate = chestplate
        self.leggings = leggings
        self.belt = belt
        self.left_glove = left_glove
        self.right_glove = right_glove
        self.boots = boots
        self.accessories = accessories

        self.rebirths = rebirths
        self.reality_shards = reality_shards
        self.training_bonus = training_bonus



    def add_exp(self, stat_name, amount): # Adds a certain amount of exp to the currently selected stat
        if hasattr(self, stat_name):
            current_exp = getattr(self, stat_name)
            if isinstance(current_exp, list): # for if its a data group and not an individual attribute dedicated for exp
                current_exp[1] = current_exp[1] + amount # index 1 of current_exp is the exp section of the data group
            else:
                setattr(self, stat_name, current_exp + amount)
        else:
            error_handling.attribute_err(stat_name)

    def level_up(self, stat_name, exp_req, exp_stat_name=None): # level up selected skill
        if hasattr(self, stat_name):
            level = getattr(self, stat_name)
            if isinstance(level, list): # checks for if its a data group or an independent attribute
                level[0] = level[0] + 1
                level[1] = level[1] - exp_req
                exp = level[1]
            else:
                setattr(self, stat_name, level + 1)
                exp = getattr(self, exp_stat_name) - exp_req
                setattr(self, exp_stat_name, exp)

            new_exp_req = self.exp_req_creation(stat_name)
            if exp > new_exp_req: # if player has exp left over and it reaches new requirement, level that skill up again
                self.level_up(stat_name, new_exp_req, exp_stat_name)
        else:
            error_handling.attribute_err(stat_name)

    def exp_req_creation(self, stat_name): # creates requirement for exp / level and returns it
        if hasattr(self, stat_name):
            level = getattr(self, stat_name)
            if isinstance(level, list):
                return self.exp_req_handling(level[0])
            return self.exp_req_handling(level)
        else:
            error_handling.attribute_err(stat_name)

    def exp_req_handling(self, level): # Calculates exp required for specific levels
        b = (level - 1) // 100
        i = (level - 1) % 100
        if b == 0:
            start_exp = 10
            end_exp = 50000
        else:
            start_exp = 50000 * (250 ** (b - 1))
            end_exp = 50000 * (250 ** b)
        return start_exp + ((i / 99) ** 2) * (end_exp - start_exp)


    def check_exp_for_up(self, stat_data_name, exp_name=None): # check current exp for selected stat and if hit exp requirement, level up the skill
        if hasattr(self, stat_data_name):
            level = getattr(self, stat_data_name)
            exp_req = self.exp_req_creation(stat_data_name) # calculate required exp for level
            if isinstance(level, list):
                if level[1] >= exp_req:
                    self.level_up(stat_data_name, exp_req)
            else:
                exp = getattr(self, exp_name)
                if exp >= exp_req:
                    self.level_up(stat_data_name, exp_req, exp_name)
        else:
            error_handling.attribute_err(stat_data_name)