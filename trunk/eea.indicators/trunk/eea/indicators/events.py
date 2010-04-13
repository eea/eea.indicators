from Products.CMFPlone.utils import getToolByName
import logging


ROLE = 'SpecificationManager' 

def delegate_manager(specification, event):
    """Handler for ISpecification -> IObjectModifiedEvent """

    new_manager = specification.getManager_user_id()
    pm = getToolByName(specification, 'portal_membership')

    roles = specification.computeRoleMap()
    for role in roles:  #remove all local grants
        if ROLE in role['local']: #XXX: change to SpecificationManager
            member_ids = [role['id'], ]

            #delete all local roles
            pm.deleteLocalRoles(obj=specification,
                                member_ids=member_ids,
                                reindex=True,)
            logging.debug("Removed all local roles for ", member_ids)

            #reasign local roles, except our interest role
            for role_id in role['local']:
                if not role_id == ROLE:
                    specification.manage_setLocalRoles(role['id'], [role_id])
                    loggin.debug("Assigned local role %s to %s" % (role_id, member_ids))

    specification.manage_setLocalRoles(new_manager, [ROLE])
    specification.reindexObjectSecurity()

    logging.debug("Added %s to %s" % (ROLE, new_manager))
