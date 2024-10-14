(define (domain query2plan)
  (:requirements :strips)

  (:types
    var - object
    var_type - object
  )

  (:predicates
    (domain_start_date ?r - var ?t - var)
    (domain_end_date ?r - var ?t - var)
    (domain_contact_topic ?r - var ?t - var)
    (domain_contact_channel ?r - var ?t - var)
    (has_type ?a - var ?t - var_type)
    (has_value ?a - var)
    (value ?a - var)
    (value_assign ?a - var ?b - var) ; 赋值 a = b
    (disable_get_info_api ?a - var)
  )

  (:action value_assignment
    :parameters (?in1 - var ?in2 - var)
    :precondition
      (and
        (has_value ?in2)
        (value_assign ?in1 ?in2)
        (not (has_value ?in1))
      )
    :effect
      (and
        (has_value ?in1)
      )
  )

  (:action get_info_api
    :parameters (?in_var - var ?in_type - var_type)
    :precondition
      (and
        (has_type ?in_var ?in_type)
        (not (has_value ?in_var))
        (not (disable_get_info_api ?in_var))
      )
    :effect
      (and
        (has_value ?in_var)
      )
  )

  (:action profit_loss_api
    :parameters (?in1 - var ?in2 - var ?out - var)
    :precondition
      (and
        (has_type ?in1 date)
        (has_value ?in1)
        (has_type ?in2 date)
        (has_value ?in2)
        (has_type ?out profit_loss_report)
        (not (has_value ?out))
      )
    :effect
      (and
        (domain_start_date ?out ?in1)
        (domain_end_date ?out ?in2)
        (has_value ?out)
      )
  )

  (:action contact_us_api
    :parameters (?in1 - var ?in2 - var ?out - var)
    :precondition
      (and
        (has_type ?in1 contact_topic)
        (has_value ?in1)
        (has_type ?in2 contact_channel)
        (has_value ?in2)
        (has_type ?out contact)
        (not (has_value ?out))
      )
    :effect
      (and
        (domain_contact_topic ?out ?in1)
        (domain_contact_channel ?out ?in2)
        (has_value ?out)
      )
  )
)
