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

            inventory=None,
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


    ):
        
        self.name = name
        self.level = level
        self.exp = exp

        self.player_class = player_class
        self.cindrals = cindrals

        self.strength = strength
        self.core_strength_data = (core_strength, core_strength_exp, current_cs_area)
        self.upper_body_data = (upper_body, upper_body_exp, current_ub_area)
        self.grip_data = (grip, grip_exp, current_grip_area)
        self.lower_body_data = (lower_body, lower_body_exp, current_lb_area)

        self.speed = speed
        self.reaction_time_data = (reaction_time, reaction_time_exp, current_rt_area)
        self.velocity_data = (velocity, velocity_exp, current_velo_area)
