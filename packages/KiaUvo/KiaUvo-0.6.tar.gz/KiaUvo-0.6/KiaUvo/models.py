class AuthToken(object):
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


class Vehicle(object):
    hood_open = False
    trunk_open = False
    front_left_open = False
    front_right_open = False
    back_left_open = False
    back_right_open = False

    door_lock_state = True

    engine = False

    last_updated = None

    def __init__(self, vehicle, status, maintenance):
        self.vehicle = vehicle
        self.status = status
        self.maintenance = maintenance

        self.hood_open = status["hoodOpen"]
        self.trunk_open = status["trunkOpen"]
        self.front_left_open = status["doorOpen"]["frontLeft"] == 1
        self.front_right_open = status["doorOpen"]["frontRight"] == 1
        self.back_left_open = status["doorOpen"]["backLeft"] == 1
        self.back_right_open = status["doorOpen"]["backRight"] == 1

        self.door_lock = status["doorLock"]

        self.engine = status["engine"]

        self.last_updated = status["lastStatusDate"]

    @property
    def all_doors_closed(self):
        return not (self.hood_open
                    or self.trunk_open
                    or self.front_left_open
                    or self.front_right_open
                    or self.back_left_open
                    or self.back_right_open)
