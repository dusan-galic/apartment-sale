import flask_restful
import flask
import model
import decorators

from schemas import (
   IntervalDate
)


class NumberApartmentsPerStatus(flask_restful.Resource):
    """

    """

    path = ['/apartments/status/report']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user):
        """
        This method should be used for getting number of apartments per status
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = IntervalDate().check_and_abort(flask.request.json or {})

        # get number of apartments per status
        apartments = model.Stan.get_num_of_apartments_per_status(
            date_from=validated_data.get('date_from'),
            date_to=validated_data.get('date_to')
        )

        # make a response
        apartments_response = {}
        for status, num_of_apartments in apartments:
            apartments_response[status] = num_of_apartments

        return apartments_response


class NumberOfSoldApartments(flask_restful.Resource):
    """

    """

    path = ['/apartments/sold/report']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user):
        """
        Report on the number of apartments sold for the period, as well as the
        difference between the projected and agreed prices.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = IntervalDate().check_and_abort(flask.request.json or {})

        # Get the number and attributes of apartments sold
        stan_count, stanovi = model.PotencijalniKupac.get_number_of_sold_apartments(
            date_from=validated_data.get('date_from'),
            date_to=validated_data.get('date_to')
        )

        # Set attribute "razlika_u_ceni" for every apartments and count "sum_razlika_u_ceni"
        sum_razlika_u_ceni = 0
        for stan in stanovi:
            razlika_u_ceni = stan.stan.cena - stan.cena_za_kupca
            setattr(stan, "razlika_u_ceni", razlika_u_ceni)
            sum_razlika_u_ceni += razlika_u_ceni

        return {
            "stan_count": stan_count,
            "sum_razlika_u_ceni": sum_razlika_u_ceni,
            "stanovi": stanovi
        }


class ReportApartmentsPKupac(flask_restful.Resource):
    """

    """

    path = ['/apartments/pkupac/<pkupac>/all']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, pkupac):
        """
        Report on all apartments for which one client is interested.
        :param current_user:
        :return:
        """

        stan_count, stanovi = model.PotencijalniKupac.get_pkupac_and_stan_by_pkupac_id(pkupac_id=pkupac)

        return {"stan_count": stan_count, "stanovi": stanovi}


class ReportApartmentsBoughtPKupac(flask_restful.Resource):
    """

    """

    path = ['/apartments/pkupac/<pkupac>/bought']

    @staticmethod
    @decorators.get_user_and_check_user_validity
    def get(current_user, pkupac):
        """
        Report on realized purchases of one client for the period.
        :param current_user:
        :return:
        """
        # Validate schema parameters
        validated_data = IntervalDate().check_and_abort(flask.request.json or {})

        status = 'kupio'
        stan_count, stanovi = model.PotencijalniKupac.get_pkupac_and_stan_by_pkupac_id_and_status(
            pkupac_id=pkupac,
            status=status,
            date_from=validated_data.get('date_from'),
            date_to=validated_data.get('date_to')
        )

        return {"stan_count": stan_count, "stanovi": stanovi}
