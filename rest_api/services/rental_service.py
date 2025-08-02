# 🔧 Service design pattern for UAV rent process

from ..models import Rental

# 🏢 Rental Business Logic
class RentalService:
    @staticmethod
    # 📝 Create new rental record
    def rent_uav(uav, renting_member, start_date, end_date):
        rental = Rental.objects.create(
            uav=uav,
            renting_member=renting_member,
            start_date=start_date,
            end_date=end_date
        )
        return rental
